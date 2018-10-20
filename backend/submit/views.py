import os
from datetime import datetime
from typing import List, Tuple

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook, load_workbook
from openpyxl.cell import Cell
from openpyxl.worksheet import Worksheet

from submit.forms import UploadFileForm

TAB_NAMES = ["Event info", "Clubs", "Fighters"]
TAB_NAMES_TOURNAMENT_TYPE = [
    "Longsword (Steel, Mixed/Men)",
    "Longsword (Steel, Women)",
    "Longsword (Nylon, Mixed)",
    "Rapier &amp; Dagger (Mixed)",
    "Single Rapier (Mixed)",
    "Sabre (Steel, Mixed/Men)",
    "Sword &amp; Buckler (Steel, Mixed)",
    "Sidesword (Steel, Mixed)",
    "Singlestick (Mixed)",
]
COMMON_MISPELLINGS = {
    "lose": "loss",
    "tie": "draw",
}


def process_workbook(workbook: Workbook) -> None:
    """ Main method to process workbook sheets. """

    sheet_names = workbook.sheetnames

    # todo: what about insensitive cases?
    if not set(TAB_NAMES).issubset(set(sheet_names)):
        raise ValidationError("Missing core tabs")

    if not set(TAB_NAMES).intersection(set(sheet_names)):
        raise ValidationError("Missing at least one tournament sheet")

    for sheet_title in sheet_names:
        remove_empty_rows(sheet_title, workbook)
        parse_cells(sheet_title, workbook)

    set_active_tab(workbook)


def set_active_tab(workbook: Workbook) -> None:
    """
    Set first tab as active by default. workbook.active should be enough but for some reason it does not deactivate
    previously selected one, so we have to iterate through them.
    """

    workbook.active = 0
    for sheet in workbook:
        if sheet.title == "Event info":
            sheet.sheet_view.tabSelected = True
        else:
            sheet.sheet_view.tabSelected = False


def remove_empty_rows(sheet_title: str, workbook: Workbook) -> None:
    """ Iterate through rows in sheet and remove when all columns have no value. """

    sheet: Worksheet
    sheet = workbook[sheet_title]
    max_row = sheet.max_row
    max_col = sheet.max_column
    rows = list(sheet.iter_rows(min_col=1, max_col=max_col, min_row=1, max_row=max_row))
    i = 1
    for row in rows:
        if not any(cell.value for cell in row):
            sheet.delete_rows(i)
        else:
            i += 1


def parse_cells(sheet_title: str, workbook: Workbook) -> None:
    """
    """
    sheet: Worksheet
    sheet = workbook[sheet_title]
    max_row = sheet.max_row
    max_col = sheet.max_column
    rows = list(sheet.iter_rows(min_col=1, max_col=max_col, min_row=1, max_row=max_row))
    for row in rows:
        cell: Cell
        for cell in row:
            remove_wrong_whitespaces(cell)
            fixes_result_name(sheet_title, cell)


def remove_wrong_whitespaces(cell: Cell) -> None:
    """
    Remove trailing and leading whitespaces when cell is string type. It also fixes all duplicated non-standard
    spaces like new line.
    """

    if cell.data_type == "s":
        cell.value = " ".join(cell.value.split())


def fixes_result_name(sheet_title: str, cell: Cell) -> None:
    """

    """

    if sheet_title in TAB_NAMES:
        return

    if cell.column in ['C', 'D']:
        if cell.data_type == "s":
            for wrong, good in COMMON_MISPELLINGS.items():
                cell.value = cell.value.replace(wrong, good)


def handle_file(uploaded_file: InMemoryUploadedFile) -> Tuple[str, List, Workbook, str]:
    """ Handle uploaded file. Calls processing method then creates new name for file with timestamp. """

    file_name = uploaded_file.name
    wb_in = load_workbook(uploaded_file)
    v_errors = []
    try:
        process_workbook(wb_in)
    except ValidationError as errors:
        v_errors = errors
    else:
        new_name = add_timestamp_to_name(file_name)

    return file_name, v_errors, wb_in, new_name


def add_timestamp_to_name(uploaded_file_name: str) -> str:
    """ Helper method which extend filename with timestamp. """

    splitted_name = os.path.splitext(uploaded_file_name)
    new_name = (
        f"{splitted_name[0]}.{datetime.now().strftime('%Y%m%d%H%M')}{splitted_name[1]}"
    )
    return new_name


def index(request: WSGIRequest) -> HttpResponse:
    """ Main view. """

    context = {}

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if "upload" in request.POST:
            if form.is_valid():

                uploaded_file = form.cleaned_data["docfile"]
                uploaded_file_name, validation_errors, wb_out, new_file_name = handle_file(
                    uploaded_file
                )
                context = {
                    "uploaded_file_name": uploaded_file_name,
                    "validation_errors": validation_errors,
                }

                if not validation_errors:
                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    response["Content-Disposition"] = (
                        "attachment; filename=" + new_file_name
                    )
                    wb_out.save(response)

                    return response

    else:
        form = UploadFileForm()

    context["form"] = form
    return render(request, "page.html", context)

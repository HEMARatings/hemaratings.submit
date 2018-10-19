import os
from copy import copy
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from openpyxl.cell import Cell
from openpyxl.worksheet import Worksheet
from submit.forms import UploadFileForm

from openpyxl import load_workbook, Workbook


tab_names = ['Event info', 'Clubs', 'Fighters']
tab_names_tournament_type = [
    'Longsword (Steel, Mixed/Men)', 'Longsword (Steel, Women)', 'Longsword (Nylon, Mixed)',
    'Rapier &amp; Dagger (Mixed)', 'Single Rapier (Mixed)', 'Sabre (Steel, Mixed/Men)',
    'Sword &amp; Buckler (Steel, Mixed)', 'Sidesword (Steel, Mixed)', 'Singlestick (Mixed)',
]


def process_workbook(workbook: Workbook):
    sheet_names = workbook.sheetnames

    # todo: what about insensitive cases?
    if not set(tab_names).issubset(set(sheet_names)):
        raise ValidationError('Missing core tabs')

    if not set(tab_names).intersection(set(sheet_names)):
        raise ValidationError('Missing at least one tournament sheet')

    for sheet_title in sheet_names:
        remove_empty_rows(sheet_title, workbook)
        remove_trailing_whitespaces(sheet_title, workbook)

    set_active_tab(workbook)


def set_active_tab(workbook):
    workbook.active = 0
    for sheet in workbook:
        if sheet.title == 'Event info':
            sheet.sheet_view.tabSelected = True
        else:
            sheet.sheet_view.tabSelected = False


def remove_empty_rows(sheet_title, workbook) -> None:
    """ """
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


def remove_trailing_whitespaces(sheet_title, workbook) -> None:
    """ """
    sheet: Worksheet
    sheet = workbook[sheet_title]
    max_row = sheet.max_row
    max_col = sheet.max_column
    rows = list(sheet.iter_rows(min_col=1, max_col=max_col, min_row=1, max_row=max_row))
    for row in rows:
        cell: Cell
        for cell in row:
            if cell.data_type == 's':
                cell.value = cell.value.strip()



def handle_file(uploaded_file):

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
    """ """

    splitted_name = os.path.splitext(uploaded_file_name)
    new_name = f"{splitted_name[0]}.{datetime.now().strftime('%Y%m%d%H%M')}{splitted_name[1]}"
    return new_name


def index(request):
    context = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if 'upload' in request.POST:
            if form.is_valid():

                uploaded_file = form.cleaned_data['docfile']
                uploaded_file_name, validation_errors, wb_out, new_file_name = handle_file(uploaded_file)
                context = {'uploaded_file_name': uploaded_file_name, 'validation_errors': validation_errors}

                if not validation_errors:
                    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = 'attachment; filename=' + new_file_name
                    wb_out.save(response)

                    return response

    else:
        form = UploadFileForm()

    context['form'] = form
    return render(request, 'page.html', context)

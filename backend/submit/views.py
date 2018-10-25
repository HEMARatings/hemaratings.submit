import os
from datetime import datetime
from typing import List, Tuple

import pycountry
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook, load_workbook
from openpyxl.cell import Cell
from openpyxl.worksheet import Worksheet

from submit.forms import UploadFileForm
from submit.workbook_validator import WorkbookValidator


def handle_file(uploaded_file: InMemoryUploadedFile) -> Tuple[str, List, Workbook, str]:
    """ Handle uploaded file. Calls processing method then creates new name for file with timestamp. """

    file_name = uploaded_file.name
    workbook = load_workbook(uploaded_file)
    v_errors = []
    new_name = add_timestamp_to_name(file_name)
    workbook_validator = WorkbookValidator(workbook=workbook)
    try:
        workbook_validator.process_workbook()
    except ValidationError as errors:
        v_errors = errors

    return file_name, v_errors, workbook, new_name


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

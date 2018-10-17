import os
from copy import copy
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from openpyxl.worksheet import Worksheet
from submit.forms import UploadFileForm

from openpyxl import load_workbook, Workbook


tab_names = ['Event info', 'Clubs', 'Fighters']
tab_names_tournament_type = [
    'Longsword (Steel, Mixed/Men)', 'Longsword (Steel, Women)', 'Longsword (Nylon, Mixed)',
    'Rapier &amp; Dagger (Mixed)', 'Single Rapier (Mixed)', 'Sabre (Steel, Mixed/Men)',
    'Sword &amp; Buckler (Steel, Mixed)', 'Sidesword (Steel, Mixed)', 'Singlestick (Mixed)',
]


def process_workbook(wb_in: Workbook):
    sheet_names = wb_in.sheetnames

    # todo: what about insensitive cases?
    if not set(tab_names).issubset(set(sheet_names)):
        raise ValidationError('Missing core tabs')

    if not set(tab_names).intersection(set(sheet_names)):
        raise ValidationError('Missing at least one tournament sheet')

    for sheet_title in tab_names:
        print('\nsheet_title ', sheet_title)
        sheet: Worksheet
        sheet = wb_in[sheet_title]

        max_row = sheet.max_row
        max_col = sheet.max_column
        rows = sheet.iter_rows(min_col=1, max_col=max_col, min_row=1, max_row=max_row)

        for i, row in enumerate(rows, start=1):

            print(i, any(cell.value for cell in row), [cell.value for cell in row])
            print([cell._value for cell in row])
            if not any(cell.value for cell in row):
                sheet.delete_rows(i)


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

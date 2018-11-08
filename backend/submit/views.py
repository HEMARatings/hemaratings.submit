import os
from datetime import datetime
from typing import List, Tuple

import pycountry
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from openpyxl import Workbook, load_workbook
from openpyxl.cell import Cell
from openpyxl.worksheet import Worksheet

from submit.forms import Step1FileUploadForm, Step2ErrorsHandlingForm, Step3EventInformation, Step4Receipt
from submit.workbook_validator import WorkbookValidator


FORMS = [
    ("file_upload", Step1FileUploadForm),
    ("errors_handling", Step2ErrorsHandlingForm),
    ("event_information", Step3EventInformation),
    ("receipt", Step4Receipt),
]

TEMPLATES = {
    "file_upload": "step1_file_upload.html",
    "errors_handling": "step2_errors_handling.html",
    "event_information": "step3_event_information.html",
    "receipt": "step4_receipt.html",
}


class SubmitWizard(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploaded_files'))
    uploaded_file = None

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step_files(self, form):
        files = super().process_step_files(form)

        if self.steps.current == 'file_upload':
            try:
                self.uploaded_file = files['file_upload-docfile']
            except KeyError:
                # todo: it shouldn't happen, but let's build some nice message
                raise
            else:
                self.fix_weak_errors()

        return files

    def done(self, form_list, form_dict, **kwargs):
        return HttpResponseRedirect('/')

    def fix_weak_errors(self):
        file_name = self.uploaded_file.name
        dirname = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{get_random_string(length=4)}"
        filename = os.path.join(dirname, file_name)

        full_path = self.storage.file_storage.path(filename)
        full_path_root, full_path_ext = os.path.splitext(full_path)
        full_path_parsed = f'{full_path_root}.parsed{full_path_ext}'
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        workbook = load_workbook(self.uploaded_file)
        workbook.save(full_path)

        workbook_validator = WorkbookValidator(workbook=workbook)
        workbook_validator.fix_automatically_errors()
        workbook.save(full_path_parsed)



#
# def index(request: WSGIRequest) -> HttpResponse:
#     """ Main view. """
#
#     context = {}
#
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#
#         if "upload" in request.POST:
#             if form.is_valid():
#
#                 uploaded_file = form.cleaned_data["docfile"]
#                 uploaded_file_name, validation_errors, wb_out, new_file_name = handle_file(
#                     uploaded_file
#                 )
#                 context = {
#                     "uploaded_file_name": uploaded_file_name,
#                     "validation_errors": validation_errors,
#                 }
#
#                 if not validation_errors:
#                     response = HttpResponse(
#                         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                     )
#                     response["Content-Disposition"] = (
#                         "attachment; filename=" + new_file_name
#                     )
#                     wb_out.save(response)
#
#                     return response
#
#     else:
#         form = UploadFileForm()
#
#     context["form"] = form
#     return render(request, "page.html", context)

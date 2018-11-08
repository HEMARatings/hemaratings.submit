from django import forms
from openpyxl import load_workbook
from submit.workbook_validator import WorkbookValidator


class Step1FileUploadForm(forms.Form):
    docfile = forms.FileField(
        required=True, label="Select a file", help_text="File to be processed"
    )

    def clean_docfile(self) -> None:
        """
        Check any serious problem which won't allow to parse file:
        * missing tabs
        * wrong file type  (TODO)
        """

        workbook = load_workbook(self.cleaned_data['docfile'])
        workbook_validator = WorkbookValidator(workbook=workbook)

        workbook_validator.check_basic_errors()


class Step2ErrorsHandlingForm(forms.Form):
    errors = forms.CharField(max_length=100)


class Step3EventInformation(forms.Form):
    event_name = forms.CharField(required=True, label="Event Name")
    # todo: date picker
    date = forms.DateField(required=True, label="Date", widget=forms.DateInput)
    # todo: dropdown
    country = forms.CharField(required=True, label="Country")
    state = forms.CharField(required=False, label="State", help_text="If applicable")
    city = forms.CharField(required=True, label="City")
    coordinates = forms.CharField(required=False, label="Coordinates", help_text="if you have them")
    organizing_club = forms.CharField(required=False, label="Organizing club", help_text="if any")
    submitter_name = forms.CharField(required=True, label="Submitter’s name")
    submitter_email = forms.EmailField(required=True, label="Submitter’s email")
    social_media_links = forms.CharField(required=False, label="Social media links")
    photo_links = forms.CharField(required=False, label="Photo links")


class Step4Receipt(forms.Form):
    errors = forms.CharField(max_length=100)



from django import forms


class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        required=True, label="Select a file", help_text="File to be processed"
    )

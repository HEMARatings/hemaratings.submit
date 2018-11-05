from django import forms


class Step1FileUploadForm(forms.Form):
    docfile = forms.FileField(
        required=True, label="Select a file", help_text="File to be processed"
    )


class Step2ErrorsHandlingForm(forms.Form):
    errors = forms.CharField(max_length=100)


class Step3EventInformation(forms.Form):
    errors = forms.CharField(max_length=100)


class Step4Receipt(forms.Form):
    errors = forms.CharField(max_length=100)



from django import forms


class UploadForm(forms.Form):
    upload_csv = forms.FileField(label='select *.csv file ', required=True)
    upload_xml = forms.FileField(label='select *.xml file ', required=True)
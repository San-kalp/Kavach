from django import forms


class sanctionForm(forms.Form):
    address = forms.CharField(label="Address",max_length=100)
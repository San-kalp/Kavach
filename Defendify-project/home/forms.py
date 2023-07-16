from django import forms

class addressForm(forms.Form):
    address = forms.CharField(label="Address" , max_length=100)
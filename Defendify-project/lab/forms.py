from django import forms




class searchForm(forms.Form):
    form_data = forms.CharField(label='' , max_length=100)


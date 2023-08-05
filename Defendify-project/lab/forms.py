from django import forms




class searchForm(forms.Form):
    form_data = forms.CharField(label="Search" , max_length=100)



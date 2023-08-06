from django import forms




class searchForm(forms.Form):
    form_data = forms.CharField(label="Search" , max_length=100)


class walletForm(forms.Form):
    wallet = forms.CharField(label="Wallet", max_length=100)


class addressForm(forms.Form):
    address = forms.CharField(label="address",max_length=100)


from django.shortcuts import render 
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from .forms import addressForm
from django.http import HttpResponseRedirect
import requests
import json
import datetime
import re

renderer = JSONRenderer()
ETHERSCAN_API_KEY = "2SFM3DIEINQ9Z7B27U9V4C4ICHUHR25R9A"


def home (request):
    form = addressForm()
    if request.method =='POST':
        form = addressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            if re.match(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",address) :
                url = "https://blockchain.info/rawaddr/%s" %address
                unspent = requests.get('https://blockchain.info/unspent?active=%s' % address).json()
                response = requests.get(url)
                data = json.loads(response.text)
                address_ = data["address"]
                amountReceived = data["total_received"]
                amountSent = data["total_sent"]
                balance = data["final_balance"]
                number_of_transactions = data["n_tx"]
                transaction = data["txs"]
                context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent]
                return render(request,"home/addressInfo.html",{'response':context})
            elif re.match(r"^0x[a-fA-F0-9]{40}$",address):
                url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
                response = requests.get(url)
                data = json.loads(response.text)
                print(data)




    context = {'form':form}
    return render(request,"home/home.html",context=context)

    
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

renderer = JSONRenderer()


def home (request):
    form = addressForm()
    if request.method =='POST':
        form = addressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
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
            # balance = (data[address]['final_balance'])/100000000
            # n_tx = data[address]['n_tx']
            # total_received = (data[address]['total_received'])/100000000
            context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent]
            return render(request,"home/addressInfo.html",{'response':context})



    context = {'form':form}
    return render(request,"home/home.html",context=context)

    
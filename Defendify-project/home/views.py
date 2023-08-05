from django.shortcuts import render 
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from .forms import searchForm, walletForm 
from django.http import HttpResponseRedirect
import requests
import json
import datetime
import re






renderer = JSONRenderer()
ETHERSCAN_API_KEY = "2SFM3DIEINQ9Z7B27U9V4C4ICHUHR25R9A"


def home (request):
    form = searchForm()
    if request.method =='POST':
        form = searchForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if len(input_data)>=10 :
                if re.match(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",input_data) :
                    url = "https://blockchain.info/rawaddr/%s" %input_data
                    unspent = requests.get('https://blockchain.info/unspent?active=%s' % input_data).json()
                    response = requests.get(url)
                    data = json.loads(response.text)
                    address_ = data["address"]
                    amountReceived = data["total_received"]
                    amountSent = data["total_sent"]
                    balance = data["final_balance"]
                    number_of_transactions = data["n_tx"]
                    transaction = data["txs"]
                    data = wallet_explorer(address=input_data).items()
                    wallet_id = get_wallet_id(address_)
                    context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent, data, wallet_id["wallet_id"]]
                    return render(request,"home/addressInfo.html",{'response':context})
                elif re.match(r"^0x[a-fA-F0-9]{40}$",input_data):
                    url = f"https://api.etherscan.io/api?module=account&action=balance&address={input_data}&tag=latest&apikey={ETHERSCAN_API_KEY}"
                    response = requests.get(url)
                    data = json.loads(response.text)
                    print(data)
                else :
                    context = get_tx_data(input_data)
                    return render(request,"home/transactionInfo.html",{'response':context})
            else :
                query = f"http://www.walletexplorer.com/api/1/firstbits?prefix={input_data}&caller=sankalp.chordia20@vit.edu"
                response = requests.get(query)
                address = json.loads(response.text)["address"]
                print(address)
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
                data = wallet_explorer(address=input_data).items()
                wallet_id = get_wallet_id(address_)
                context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent, data, wallet_id["wallet_id"]]
                return render(request,"home/addressInfo.html",{'response':context})

    context = {'form':form}
    return render(request,"home/home.html",context=context)



def wallet_explorer(address):
    query = f"http://www.walletexplorer.com/api/1/address-lookup?address={address}&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)


def get_tx_data(txid):
    query = f"http://www.walletexplorer.com/api/1/tx?txid={txid}&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)

def get_wallet_id(address):
    query = f"http://www.walletexplorer.com/api/1/address?address={address}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)


def wallet(request):
    form = walletForm()
    context={'form':form}
    return render(request,"home/wallet.html",context=context)

def wallet_detail(request, wallet):
    query = f"http://www.walletexplorer.com/api/1/wallet-addresses?wallet={wallet}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    data = json.loads(requests.get(query).text)
    return render(request,"home/wallet_detail.html",{'response':data})

def wallet_transactions(request, wallet):
    query = f"http://www.walletexplorer.com/api/1/wallet?wallet={wallet}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    data = json.loads(requests.get(query).text)
    return render(request,"home/wallet_detail_transactions.html",{'response':data})










from django.shortcuts import render 
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from .forms import searchForm, walletForm , addressForm
from django.http import HttpResponseRedirect
import requests
import json
import datetime
import re
import logging
from web3 import Web3

renderer = JSONRenderer()
ETHERSCAN_API_KEY = "2SFM3DIEINQ9Z7B27U9V4C4ICHUHR25R9A"
INFURA_API_KEY: str = "7880212ac22945e58ba986a0d644f84e"

regex_patterns = [
        (r'^(bc1)[a-zA-HJ-NP-Z0-9]{25,39}$','Bitcoin Bech 32 Address', range(25,35)), #Have to resolve the issue
        (r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', 'Bitcoin Legacy (P2PKH) Address', range(25, 35)),
        (r'^1\x00([a-km-zA-HJ-NP-Z1-9]\x00){25,34}$', 'Bitcoin Legacy (P2PKH) Address with Null Bytes', range(25, 35)),
        (r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', 'Bitcoin P2SH Address', range(25, 35)),
        (r'^3\x00([a-km-zA-HJ-NP-Z1-9]\x00){25,34}$', 'Bitcoin P2SH Address with Null Bytes', range(25, 35)),
        (r'^6P[a-km-zA-HJ-NP-Z1-9]{56}$', 'Bitcoin Private Key (WIF) Compressed', range(56, 57)),
        (r'^6\x00P\x00([a-km-zA-HJ-NP-Z1-9]\x00){56}$', 'Bitcoin Private Key (WIF) Compressed with Null Bytes', range(56, 57)),
        (r'^5[a-km-zA-HJ-NP-Z1-9]{50}$', 'Bitcoin Private Key (WIF) Uncompressed', range(50, 51)),
        (r'^5\x00([a-km-zA-HJ-NP-Z1-9]\x00){50}$', 'Bitcoin Private Key (WIF) Uncompressed with Null Bytes', range(50, 51)),
        (r'^[KL][a-km-zA-HJ-NP-Z1-9]{51}$', 'Bitcoin Extended Private Key (xprv) or Extended Public Key (xpub)', range(51, 52)),
        (r'^[KL]\x00([a-km-zA-HJ-NP-Z1-9]\x00){51}$', 'Bitcoin Extended Private Key (xprv) or Extended Public Key (xpub) with Null Bytes', range(51, 52)),
        (r'^xprv[a-km-zA-HJ-NP-Z1-9]{107,108}$', 'Bitcoin BIP-32 Extended Private Key (xprv)', range(107, 109)),
        # (r'^x\x00p\x00r\x00v\x00([a-km-zA-HJ-NP-Z1-9]\x00){107,108}$', 'Bitcoin BIP-32 Extended Private Key (xprv) with Null Bytes', range(107, 109)),
        (r'^xpub[a-km-zA-HJ-NP-Z1-9]{107,108}$', 'Bitcoin BIP-32 Extended Public Key (xpub)', range(107, 109)),
        # (r'^x\x00p\x00u\x00b\x00([a-km-zA-HJ-NP-Z1-9]\x00){107,108}$', 'Bitcoin BIP-32 Extended Public Key (xpub) with Null Bytes', range(107, 109))

        (r'^X[a-km-zA-HJ-NP-Z1-9]{33}$', 'Dash', range(33, 34)),
        (r'^D[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{32}$', 'Doge', range(34, 35)),
        (r'^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$', 'Litecoin', range(26, 34)),
        (r'^r[0-9a-zA-Z]{24,34}$', 'Ripple', range(24, 35)),
        (r'^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$', 'Monero Pattern 1', range(95, 96)),
        (r'^[48][0-9AB]|4[1-9A-HJ-NP-Za-km-z]{12}(?:[1-9A-HJ-NP-Za-km-z]{30})?[1-9A-HJ-NP-Za-km-z]{93}$', 'Monero Pattern 2', range(95, 96)),
        (r'^0x[a-fA-F0-9]{40}$', 'Ethereum', range(42, 43))
    ]


def home (request):
    form = searchForm()
    aform = addressForm()
    if request.method == 'POST' and request.POST.get('coin_type') == "bitcoin":
        form = searchForm(request.POST)
        aform = addressForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if len(input_data) >=10 :
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
                else:
                    context = get_tx_data(input_data)
                    return render(request,"home/transactionInfo.html",{'response':context})
            else:
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
            

        if aform.is_valid():
            address = aform.cleaned_data['address']
            for pattern, pattern_name, length_range in regex_patterns:
                 if re.match(pattern, address) and len(address) in length_range:
                     print(pattern, "\t" , pattern_name)

    elif request.method == 'POST' and request.POST.get('coin_type') == "ethereum":
        form = searchForm(request.POST)
        aform = addressForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if len(input_data) >= 10:
                if re.match(r"^0x[a-fA-F0-9]{40}$", input_data):
                    try:
                        infura_url = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
                        w3 = Web3(Web3.HTTPProvider(infura_url))

                        if not w3.is_address(input_data):
                            raise ValueError(f"The address {input_data} is not valid")

                        input_data_c = Web3.to_checksum_address(input_data)


                        # Get balance of the address in Ether
                        balance = w3.eth.get_balance(input_data_c) / 10**18

                        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={input_data}&startblock=0&endblock=99999999&page=1&offset=100&sort=desc&apikey={ETHERSCAN_API_KEY}"
                        response = requests.get(url)
                        transactions = response.json()['result']
                        number_of_transactions = len(transactions)

                        # You can now use the transactions list to calculate total_received and total_sent
                        total_received = 0
                        total_sent = 0
                        for transaction in transactions:
                            value = int(transaction['value']) / 10**18  # Convert Wei to Ether
                            if transaction['to'] == input_data:
                                total_received += value
                            if transaction['from'] == input_data:
                                total_sent += value

                        context = [input_data, total_received, total_sent, balance, number_of_transactions, transactions]
                        return render(request, "home/addressInfo.html", {'response': context})

                    except requests.exceptions.RequestException as e:
                        error_message = f"An error occurred while fetching data: {e}"
                        return HttpResponse('error_message: {}'.format(error_message))
                    except KeyError:
                        error_message = "Data format error: Key not found in the response."
                        return HttpResponse('error_message: {}'.format(error_message))

                else:
                    url = "https://api.blockchair.com/ethereum/dashboards/transaction/%s" % input_data
                    response = requests.get(url)
                    data = response.json()
                    if data and "data" in data and input_data in data["data"]:
                        transaction = data["data"][input_data]
                        context = [transaction]
                        return render(request, "home/transactionInfo.html", {'response': context})
                    else:
                        return HttpResponse("Unable to retrieve Ethereum transaction.")
            else:
                return HttpResponse("Fuzzy search is not supported for Ethereum addresses.")


    elif request.method == 'POST' and request.POST.get('coin_type') == "dogecoin":
        form = searchForm(request.POST)
        aform = addressForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if len(input_data) >= 10:
                try:
                    # Get balance of the address in Dogecoin
                    url = f"https://dogechain.info/api/v1/address/balance/{input_data}"
                    response = requests.get(url)
                    balance = float(response.json()['balance'])

                    # Get received and sent amount of the address
                    url = f"https://dogechain.info/api/v1/address/received/{input_data}"
                    response = requests.get(url)
                    total_received = float(response.json()['received'])

                    url = f"https://dogechain.info/api/v1/address/sent/{input_data}"
                    response = requests.get(url)
                    total_sent = float(response.json()['sent'])

                    # Get transactions of the address
                    url = f"https://dogechain.info/api/v1/address/transactions/{input_data}"
                    response = requests.get(url)
                    transaction_hashes = response.json()['transactions']

                    # Get detailed information for each transaction
                    transactions = []
                    for tx_hash in transaction_hashes:
                        url = f"https://dogechain.info/api/v1/transaction/{tx_hash}"
                        response = requests.get(url)
                        transactions.append(response.json())

                    # Get number of transactions
                    number_of_transactions = len(transactions)

                    # Get unspent transactions
                    url = f"https://dogechain.info/api/v1/address/unspent/{input_data}"
                    response = requests.get(url)
                    unspent_transaction_hashes = response.json()['unspent_outputs']

                    # Get detailed information for each unspent transaction
                    unspent_transactions = []
                    for tx_hash in unspent_transaction_hashes:
                        url = f"https://dogechain.info/api/v1/transaction/{tx_hash}"
                        response = requests.get(url)
                        unspent_transactions.append(response.json())

                    # Get wallet id
                    # Note: The Dogechain API does not provide a direct way to get the wallet id. 
                    # If the wallet id is included in the transaction data, you can extract it from there.
                    # For example, if the wallet id is included in the 'script' field of the transaction data:
                    wallet_id = transactions[0]['script'] if transactions else None

                    # Note: The Dogechain API does not provide a method to fetch transactions of an address

                    context = [input_data, total_received, total_sent, balance]
                    return render(request, "home/addressInfo.html", {'response': context})

                except requests.exceptions.RequestException as e:
                    error_message = f"An error occurred while fetching data from {url}: {e}"
                    
                except KeyError as e:
                    error_message = f"Data format error: Key {e} not found in the response."
                
                except ValueError as e:
                    error_message = f"Conversion error: {e}"

                except Exception as e:
                    error_message = f"Unknown error: {e}"

                finally:
                    return HttpResponse('error_message: {}'.format(error_message))
            else:
                return HttpResponse("Fuzzy search is not supported for Dogecoin addresses.")
        
    context = {'form': form, 'aform': aform}
    return render(request, "home/home.html", context=context)


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




import requests
# from ens import ENS
# from web3 import Web3


bscscan_api = "MVA9TJPP2RF745ST4I2H1K2VKB6JHX5GVE"
etherscan_api = "62MUC883JQFRD3KSMATEQ7QI4PRGU6MYKJ"
polygonscan_api = "D5KVD3HS84XCDTNBNTSRIM6E2Y931YA666"

opensea_api = "bcfb694364904325aba903d23150ed5b"
rarible_api = "71e09730-14ca-4c2c-95f1-90960114b4dc"

ALCHEMY_KEY = "Lb-ogSNqXaBue93deN155EnXCIdMCO5H"


def start():
	print("-----------WEB3 OSINT tool-------------")
	print("\n[+] Supported EVM Chains \n |-Ethereum \n |-Polygon \n |-Binance Smart Chain ")
	print()
	wallet_address = input("Wallet Address : ")
	# wallet_address = "0x66856aF51D80a2e564d3651703b298517F07c7Db"
	# wallet_address = "0x77c0c1c3d55a9afad3ad19f231259cf78a203a8d"
	# wallet_address = "0xCcA767b41a4a15Ff38558e9F1870456eC4cC87C3" #FINE
	# wallet_address = "0x07f7dED89D22c4BABa44346577ceBCBB9D1dB81D" #someOG azuki holder
	# wallet_address = "0x7bfee91193d9df2ac0bfe90191d40f23c773c060" #debank no1 social rank	
	return wallet_address



def check_social_protocol(wallet_address):


	alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}"
	w3 = Web3(Web3.HTTPProvider(alchemy_url))
	ns = ENS.fromWeb3(w3)

	wallet_name = ns.name(wallet_address)

	print(wallet_name)

	




def check_exchanges(wallet_address):

	print("\n------------ [Exchanges] ------------")

	print("[*] we have to setup active monitoring script with persistant storage for UNISWAP")
	print("[*] we have to setup active monitoring script with persistant storage for Pancake Swap")
	print("[*] we have to setup active monitoring script with persistant storage for Trader Joe ")

def check_nft_marketplace(wallet_address):
	
	print("\n------------ [NFT Marketplace] ------------")


	opensea_url = f"https://api.opensea.io/api/v2/accounts/{wallet_address}"

	headers = {"accept": "application/json","x-api-key": opensea_api}

	response = requests.get(opensea_url, headers=headers)

	# print(response.json())
	if "errors" not in response.json():
		print("[+] active on opensea") 





	rarible_url = f"https://api.rarible.org/v0.1/items/byOwner?blockchains=ETHEREUM&owner=ETHEREUM:{wallet_address}"

	headers = {"accept": "application/json", "X-API-KEY": rarible_api}

	response = requests.get(rarible_url, headers=headers)

	# print(response.json())

	if len(response.json()["items"]) != 0:
		print("[+] active on rarible")
	else:
		print("[+] not active on rarible")




def check_chain_activity(wallet_address):

	print("\n------------ [Chains] ------------")

	ethurl = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={etherscan_api}")
	
	# print(ethurl.json()["status"])

	if ethurl.json()["status"] != "0":
		print("[+] active on Ethereum")
	else:
		print("[-] not active on Ethereum")


	bscurl = requests.get(f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={bscscan_api}")

	# print(bscurl.text)

	if bscurl.json()["status"] != "0":
		print("[+] active on Binance Smart Chain")
	else:
		print("[-] not active on Binance Smart Chain")

	polyurl = requests.get(f"https://api.polygonscan.com/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={polygonscan_api}")

	# print(polyurl.text)

	if polyurl.json()["status"] != "0":
		print("[+] active on Polygon")
	else:
		print("[-] not active on Polygon")

def osint(wallet_address):
	check_chain_activity(wallet_address)
	check_nft_marketplace(wallet_address)
	# check_exchanges(wallet_address)
	# check_social_protocol(wallet_address)


def get_collection(collection_name):

	url = f"https://api.opensea.io/api/v2/collections/{collection_name}"

	headers = {
	    "accept": "application/json",
	    "x-api-key": opensea_api
	}

	response = requests.get(url, headers=headers)

	# print(response.json()["discord_url"])
	if len(response.json()["discord_url"]) != 0:
		discord_server = response.json()["discord_url"]
		print(f" |- collection's discord url : {discord_server}")

def nft_osint(wallet_address):

	print("\n\n------------ [post NFT OSINT] ------------")

	opensea_url = f"https://api.opensea.io/api/v2/accounts/{wallet_address}"

	headers = {"accept": "application/json","x-api-key": opensea_api}

	response = requests.get(opensea_url, headers=headers)

	# print(response.json())

	if len(response.json()["bio"]) != 0:
		bio =(response.json()["bio"])
		print(f"[+] USER opensea BIO FOUND : {bio}")

	if len(response.json()["username"]) != 0:
		username =(response.json()["username"])
		print(f"[+] opensea USERNAME FOUND : {username}")

	if len((response.json())["social_media_accounts"]):
		social_medias = response.json()["social_media_account"]
		for x in range(len(social_medias)):
			print(f"[+] FOUND SOCIAL MEDIAS : {social_medias[x]}")


	url = f"https://api.opensea.io/api/v2/chain/ethereum/account/{wallet_address}/nfts"

	headers = {"accept": "application/json","x-api-key": opensea_api}

	response = requests.get(url, headers=headers)

	# print(response.json())
	# print(response.json()["nfts"])
	if len(response.json()["nfts"]) != 0:
		print("[+] NFT's Found on Ethereum")

	for x in range(len(response.json()["nfts"])):
		collection = response.json()["nfts"][x]["collection"]
		name = response.json()["nfts"][x]["name"]
		print(f"[+] NFT found on opensea : {name}::{collection}")
		get_collection(collection)


	url = f"https://api.opensea.io/api/v2/chain/matic/account/{wallet_address}/nfts"

	headers = {"accept": "application/json","x-api-key": opensea_api}

	response = requests.get(url, headers=headers)

	# print(response.json())
	# print(response.json()["nfts"])
	# print(len(response.json()["nfts"]))

	if len(response.json()["nfts"]) != 0:
		print("[+] NFT's Found on Polygon")

	for x in range(len(response.json()["nfts"])):
		collection = response.json()["nfts"][x]["collection"]
		name = response.json()["nfts"][x]["name"]
		print(f"[+] NFT found on opensea : {name}::{collection}")
		get_collection(collection)


wallet = start()
osint(wallet)
nft_osint(wallet)


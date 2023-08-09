import requests

url = "https://api.trmlabs.com/public/v1/sanctions/screening"

payload = {}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)
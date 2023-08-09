import requests
import json

list1 = ['13o5rKbr74wnaSANaMwWWYMhyhNLSXckEz',
'c371eb6820214043060538ef4f79b796607c63f73b9a74bf6a4fdf1c1c63ef19',
'1ArG3JwEbF4WrCiEnXQXUAgQumAVzqnQHD',
'1697wz4hwVXNqNa7WaAVyLQ8UAdLP3JyNA',
'1GByuTyJ22vmQQbnCjeenMg8jc38EruRwH',
'191S2U9goEjsEtn93ZmmaqWg8DVzLBEeRx',
'187QAeVKNNp7vZARX8De3KkZGwRkrXA9tt',
'c7eb28c30d8b23e0612b1678a2ca1cd879655eda3e9f190ea3f6f67a176e475d',
'17fcFGZEHQFysZKxscwrro7L8ek5iUJJuy',
'1JesnRQvEGSXc6WEH6apb2pSEHoT5aUdAt',
'1GgTmTqxMzaSHZ6QQWAUchdL8p1Csf9RzW',
'1FGV4DK8hpxfSKzgCZKcqGVosK8AW1UHVb',
'1Awxsf2rrxcNXKs7LZ4F6kWcqiQQ6DfZHJ',
'1MPkxvk2q7moUpGtb3susNpLYMzkEbGHTk',
'1HJpTzj6We86ii8dfZU8LAS4d2EPzwSpij',
'1ANeJQbuuDxBATkWRaHL378EczzbA1zUyu',
'1DwMTEqjHH2W4nM4RSxRFqmXDWjeFqwco4',
'1EqmnkqcN9MQzPLH8zVMGeJwicENe9PQhz',
'17ntkxB2zw4pxRGxNhbNtPkQ4q52C3rVmm',
'13NiprJfpxzapH8Tur8We435DyHERTtAxx',
'1BasYRJ92LLJQj1rY1KHsmtMfTctVfmArG',
'1FFDQFskAC9mofEsQ3MJAWeRFG94QJsF3s',
'1BeBocgsgqJeQT7jZi8RyAZFDCAhZ6uhYL',
'1F3hTbJhM6XNJbQ5PKzpQXsuhyiNaeV4Ci',
'1HCmLugk1DNjGZbY7PhHFTybc3r7FxfQPJ',
'1ANiaLBdMutnhsCmNEXJQJ2HYqjTX9SFQD',
'1MWmEDAZ8iM78BjXTkAWNW2ahBGFjAsWGu',
'19vPgWWciZXt6DxYBvJqiP1WDWG8V5H5mo',
'17LB7cnHPyXvQGSjDYNZoZFu7J5GWXQBsy',
'1BEE14BzPNwc77eVhkt6ttGdWSty2rfiTX',
'1NvGdS2J7GG79HVXiBFdhCQiswaE9vAjGJ',
'1DoiDRUaMneF4VHjRVgto4fnsbGg8zqhez',
'15iqiTNF1dmizNmTf47vnrfQ5teH1XTkxa',
'1KtzDrav6efrCC4gJuzxvfrw6ZHNRRgGgY',
'12rKFBnou4eCCzPuQDdNobnNCpTNt6j7x3',
'1QAwFqQZEBjyHnNyQp3vPsGZ4Eip5GUWyS',
'1KYY7xvDxKDe262iR3xBLHaBwX1DKf9Pxv',
'1ArFuLxoej3n7P34Nq1Cfic1C3ieXTZf8v',
'1JvmE3c9fLSFmC3De6B9HrHxNiGpiE1WUZ',
'1VQt2LkkzAGJE4r64h3SAA3wMEe35vduQ',
'1P3g7xZhVmC2TTfxtuVxWCTDtzf2w89Rix',
'1H5ppG868MYspbWLfuRSrKc8ev4qNRzgi8',
'1CytbjiYfx62SJbnB1Xs28LTMwS91uxZPM',
'16SMDJzPAHLP9PxGkDkUqy959ygkENhGos',
'14r2Kyn3gBdP12Gx17Qf4BPAq6hbaDa244',
'1BnfV3GmMQwG1Bs8JmUbrxFkGvU25HLKyh',
'188zgBZy5ed7ehAKG7Nuo54toJddgvS9eL',
'1KDDhJLFiqoN2JyTb9aUBWwvKHhvqCEni9',
'15gUvKo4Tvwp2c2xW751VnmCDFkFnqePEs',
'95d36a6926639ba50d02f190d3ca2f9322ce721502d47b32a1e8d8be1b13cb40',
'409803bb5e124fd028c0482027c7722e84ce55b78204b279d3a44aba5e7c1698',
'1Jkp6RupCtoRvKkAtAh8yRtNJoi8ogMtie',
'1Ej4Jm8J83tKG4wUAbikNF3rQoGckH4Emp',
'LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd']

headers = {
    'X-API-Key': '23da073652dd9901d0644cddf8ab7de0b422456d0eacc0fc663a3cb204e79709',
    'Accept': 'application/json',
}


for item in list1 :
    url = f"https://public.chainalysis.com/api/v1/address/{item}"
    response = requests.get(url,headers= headers)
    data = json.loads(response.text)
    print(data)
    

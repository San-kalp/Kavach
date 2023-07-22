import json
import requests
import datetime
import csv 

ETHERSCAN_API_KEY = "2SFM3DIEINQ9Z7B27U9V4C4ICHUHR25R9A"

# url = f"http://api.etherscan.io/api?module=account&action=txlist&address=0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
# data = requests.get(url)


# parsed_json = json.loads(data.text)


# address = "0x1f9090aae28b8a3dceadf281b0f12828e676c326"
# # Extract the "blockNumber" and "timeStamp" from the "result" list
# block_number_list = [item["blockNumber"] for item in parsed_json["result"]]
# time_stamp_list = [item["timeStamp"] for item in parsed_json["result"]]
# time_stamp=[]
# for time in time_stamp_list:
#     time_stamp.append(str(datetime.datetime.fromtimestamp(int(time))))

# block_timestamp_dict = dict(zip(block_number_list, time_stamp_list))


# received_hashes = [item["hash"] for item in parsed_json["result"] if item["to"] == address]
# sent_hashes = [item["hash"] for item in parsed_json["result"] if item["from"] == address]
# received_hashes_timestamp_dict = dict(zip(received_hashes, time_stamp))
# sent_hashes_timestamp_dict = dict(zip(sent_hashes,time_stamp))

# print(received_hashes_timestamp_dict)


def transaction_hash_and_time_stamp(address,choice):
    url = f"http://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    data = requests.get(url)
    parsed_json = json.loads(data.text)
    # for item in parsed_json["result"] : 
    #     print(item["from"].__eq__(address.lower()))
    #Have to add lower because of matching issues
    time_stamp_list_sent = [item["timeStamp"] for item in parsed_json["result"] if item["from"].__eq__(address.lower()) ]
    time_stamp_list_received = [item["timeStamp"] for item in parsed_json["result"] if item["to"].__eq__(address.lower()) ]
    time_stamp_sent=[]
    for time in time_stamp_list_sent:
     time_stamp_sent.append(str(datetime.datetime.fromtimestamp(int(time))))

    time_stamp_received=[]
    for time in time_stamp_list_received:
     time_stamp_received.append(str(datetime.datetime.fromtimestamp(int(time))))



    received_hashes = [item["hash"] for item in parsed_json["result"] if item["to"].__eq__(address.lower())]
    sent_hashes = [item["hash"] for item in parsed_json["result"] if item["from"].__eq__(address.lower())]


    if choice == "received":
    #  received_hashes_timestamp_dict = dict(zip(received_hashes, time_stamp))
     received_transactions_list = [{"Hash": hash_val, "Timestamp": timestamp} for hash_val, timestamp in zip(received_hashes, time_stamp_received)]
     field = ['Hash','Timestamp']  
     filename = "Received.csv"
     with open(filename,'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=field)
        writer.writeheader()
        writer.writerows(received_transactions_list)
     return "Done"
    
    elif choice == "sent":
             sent_transactions_list = [{"Hash": hash_val, "Timestamp": timestamp} for hash_val, timestamp in zip(sent_hashes, time_stamp_sent)]
             field = ['Hash','Timestamp']  
             filename = "Sent.csv"
             with open(filename,'w') as csvfile:
                 writer = csv.DictWriter(csvfile,fieldnames=field)
                 writer.writeheader()
                 writer.writerows(sent_transactions_list)
    



list1= transaction_hash_and_time_stamp(address="0x4c9AF439b1A6761B8E549D8d226A468a6b2803A8",choice="sent")

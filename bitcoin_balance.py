import os.path 
import urllib.request
import json  

detain = input("Enter the path to your 'address' file")

if os.path.exists(detain.strip()):
    data = open (detain,'r')
    outfile = open("balances.txt",'w')

    for line in data :
        bal = "https://blockchain.info/balance?active=%s" %line


        balance = urllib.request.urlopen(bal)


        data2 = json.loads(balance.read())

        outfile.write(str(data2) +"\n")
    
    outfile.close()

    data.close()

else :
    print("Invaid path")



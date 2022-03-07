import pandas as pd
import time
import json
import requests


holder_data = {'wallet': [], 'balance': [], '1st-txdate': [], 'erc20': [], 'erc20tokenContractAddress': [], 'erc20tokenName': [], 'erc20tokenSymbol': [],
               'erc20tokenBalance': [], 'erc721': [], 'erc721tokenContractAddress': [], 'erc721tokenName': [], 'erc721tokenSymbol': [], 'erc721tokenBalance': []}


rejects = []


            


            


def getTransactions(address):
    transcations = requests.get("https://blockscout.com/eth/mainnet/api?module=account&action=txlist&sort=asc&startblock=0&endblock=99999999&address=" + address)
    txs = transcations.json()
    if txs['status'] == '1':
        
            trs = txs['result'][0]['timeStamp']
            my_time= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(trs)))
            holder_data['1st-txdate'].append(my_time)
            print(my_time)
    else:
        holder_data['1st-txdate'].append('no transcation')
        print("no transcation")



def tokenlist(address):
    tokenz = requests.get("https://blockscout.com/eth/mainnet/api?module=account&action=tokenlist&address=" + address)
    tokenz_json = tokenz.json()
    if tokenz_json['status'] == '1':
        for token in tokenz_json['result']:
            print(holder_data.json())
            if token['type'] == 'ERC-20':
                print(token["symbol"])
                
                holder_data['erc20tokenContractAddress'].append(token['ContractAddress'])
                holder_data['erc20tokenName'].append(token['name'])
                holder_data['erc20tokenSymbol'].append(token['symbol'])
                holder_data['erc20tokenBalance'].append(token['balance'])
            elif token['type'] == 'ERC-721':
                
                holder_data['erc721tokenContractAddress'].append(token['ContractAddress'])
                holder_data['erc721tokenName'].append(token['name'])
                holder_data['erc721tokenSymbol'].append(token['symbol'])
                holder_data['erc721tokenBalance'].append(token['balance'])
            else:
                print("not a token")
    else:
        holder_data['erc20'].append('no token')

    


def getAddresses():
    with open('Poolsuite-Executive-Member.csv', 'r') as f:
        addrbal = pd.read_csv(f, usecols=[0,2])
        for line in addrbal['balance']:
            holder_data['balance'].append(line)
        for line in addrbal['address']:
            holder_data['wallet'].append(line)
            try:
                getTransactions(line)
                time.sleep(2)
            except:
                print("transcation error")
                rejects.append(line)
            try:
                tokenlist(line)
            except:
                print("token error")
                print(holder_data)
                rejects.append(line)

            with open('rejects.txt', 'w') as f:
                for line in rejects:
                    f.write(line)
                    f.write('\n')
    return holder_data



def main():
    getAddresses()
    with open('holder_data.json', 'w') as f:
        json.dump(holder_data, f)
    df = pd.DataFrame(holder_data)
    df.to_csv('data_exec.csv', index=False)


if __name__ == '__main__':
    main()
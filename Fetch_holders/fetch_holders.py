#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 13:21:39 2021

@author: algokittens
"""
import pandas as pd
from algosdk.v2client import algod
from algosdk.v2client import indexer


pk = "GANGAAWKBJBWQJIIETTLWQT7ZFGPC4UDIITNGP55BCQPB26IEMOPOHQMEA"
path_out = "/home/algokittens/GANG_holders.csv"
testnet = False


if (testnet==False):    
    indexer_address = "https://algoexplorerapi.io/idx2"


elif (testnet==True):
    indexer_address = "https://testnet.algoexplorerapi.io/idx2"


algod_token = ""

headers = {'User-Agent': 'py-algorand-sdk'}

myindexer = indexer.IndexerClient(indexer_token="", headers=headers, indexer_address=indexer_address)

response = myindexer.account_info(
    address=pk)


df = pd.DataFrame(response['account']['assets'])
d = df.loc[(df.deleted == False)]
d = d.loc[(d.amount == 0)]

asset_ids = list(d['asset-id'])

def fetch_account (asset_id):

    response = myindexer.asset_balances(asset_id)
    
    df = pd.DataFrame(response['balances'])
    df['asset_id']=asset_id
    
    d = df.loc[(df.amount == 1)]
        
    return(d)


addresses = []
for j in range(0,len(asset_ids)):
    addresses.append(fetch_account(asset_ids[j]))
    
    
d = pd.concat(addresses, axis=0)
d = d[['asset_id', 'address']]
d.to_csv(path_out, index=False)

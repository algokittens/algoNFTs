#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 19:11:29 2021

@author: algokittens
"""
from algosdk.future.transaction import AssetTransferTxn
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.algod_helper import wait_for_confirmation, print_asset_holding
import pandas as pd

settings = Settings('batch_remove')
algod_client = settings.get_algod_client()
sk = settings.get_private_key()
pk = settings.get_public_key()



def remove_asset(asset_id):
    
    asset_id = int(asset_id)

    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    
    txn = AssetTransferTxn(
        sender=pk,
        sp=params,
        close_assets_to=pk,
        receiver=pk,  
        amt=0,  
        index=asset_id)
        
    stxn = txn.sign(sk)
    txid = algod_client.send_transaction(stxn)
    print(txid)
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid)




if(settings.remove_all == "False"):
    with open(settings.input_path) as csv_file:
        data = [line.rstrip() for line in csv_file]

    for n in range(0, len(data)):
        remove_asset(data[n])

elif(settings.remove_all=="True"):
    myindexer = settings.get_indexer()
    response = myindexer.account_info(
        address=pk)

    df = pd.DataFrame(response['account']['assets'])
    data = df.loc[(df.amount == 0)]


    for n in range(0, len(data)):
        remove_asset(data.iloc[n]['asset-id'])
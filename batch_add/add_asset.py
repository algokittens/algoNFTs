#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 19:11:29 2021

@author: phyto
"""
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()


def add_asset (asset_id, m, testnet=True):
    asset_id = int(asset_id)
    pk =  mnemonic.to_public_key(m)
    sk = mnemonic.to_private_key(m)
    
    
    if (testnet==True):
        algod_address = "https://api.testnet.algoexplorer.io"
    elif (testnet==False):
        algod_address = "https://api.algoexplorer.io"
        
    algod_token = ""
    headers = {'User-Agent': 'py-algorand-sdk'}
    algod_client = algod.AlgodClient(algod_token, algod_address, headers);    
    status = algod_client.status()
    
    
    
    def wait_for_confirmation(client, txid):
        last_round = client.status().get('last-round')
        txinfo = client.pending_transaction_info(txid)
        while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
            print("Waiting for confirmation")
            last_round += 1
            client.status_after_block(last_round)
            txinfo = client.pending_transaction_info(txid)
        print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
        return txinfo


    def print_asset_holding(algodclient, account, assetid):
        account_info = algodclient.account_info(account)
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1        
            if (scrutinized_asset['asset-id'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                print(json.dumps(scrutinized_asset, indent=4))
                break   
    
    # OPT-IN
    
    # Check if asset_id is in account 3's asset holdings prior
    # to opt-in
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    
    account_info = algod_client.account_info(pk)
    holding = 0
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            print("asset " + str(asset_id) +" already added")
            break
    
    if not holding:
    
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=pk,
            sp=params,
            receiver=pk,
            amt=0,
            index=asset_id)
        stxn = txn.sign(sk)
        txid = algod_client.send_transaction(stxn)
        print(txid)
        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, pk, asset_id)
        
        
asset_ids = os.getenv('asset_ids')
add_this = np.loadtxt(asset_ids)
m = os.getenv('m')
testnet= eval(os.getenv('testnet'))

for n in range(0, len(add_this)):
    add_asset(add_this[n], m, testnet)

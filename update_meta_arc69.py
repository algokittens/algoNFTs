#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:51:00 2021

@author: algokittens
"""

import json
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future.transaction import AssetConfigTxn
import pandas as pd 


def update_meta (n, csv_path, mnemonic1, external_url, description, algod_token, update_NFT=True, testnet=True):
    
    df = pd.read_csv(csv_path)    
    
    if (testnet==True):
       algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    elif (testnet==False):
       algod_address = "https://mainnet-algorand.api.purestake.io/ps2" 
       
    asset_id = df['ID'][n]
    
    d = df.drop(['ID'], axis=1)
    
    items = d.iloc[n]
    items = items[items != "None"]
    
    l = []
    
    for n in range(0,len(items)):
        l.append({
      "trait_type": items.index[n],
      "value": items[n]}
    )
    
    out = json.dumps(l)
    
    
    if (external_url==""):
        if (description==""):
            meta_data = '{"standard":"arc69", "attributes":' + out + '}' 
        else:
            meta_data = '{"standard":"arc69", "description":"' + description + '","attributes":' + out + '}' 
            
    else:
        if (description==""):
            meta_data = '{"standard":"arc69"' + ',"external_url":"' + external_url + '","attributes":'  + out + '}' 
            meta_data = meta_data.replace("'", '"')                
            
        else:
            meta_data = '{"standard":"arc69"' + ',"external_url":"' + external_url + '","description":"' + description + '","attributes":'  + out + '}' 
            meta_data = meta_data.replace("'", '"')    
    

    
    print(meta_data)
    
    pk = mnemonic.to_public_key(mnemonic1)
    sk = mnemonic.to_private_key(mnemonic1)
    
    headers = {
        "X-API-Key": algod_token,
    }
    
    algod_client = algod.AlgodClient(algod_token, algod_address, headers);
    
    
    def wait_for_confirmation(client, txid):
        """
        Utility function to wait until the transaction is
        confirmed before proceeding.
        """
        last_round = client.status().get('last-round')
        txinfo = client.pending_transaction_info(txid)
        while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
            print("Waiting for confirmation")
            last_round += 1
            client.status_after_block(last_round)
            txinfo = client.pending_transaction_info(txid)
        print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
        return txinfo
    
    #   Utility function used to print created asset for account and assetid
    def print_created_asset(algodclient, account, assetid):    
        # note: if you have an indexer instance available it is easier to just use this
        # response = myindexer.accounts(asset_id = assetid)
        # then use 'account_info['created-assets'][0] to get info on the created asset
        account_info = algodclient.account_info(account)
        idx = 0;
        for my_account_info in account_info['created-assets']:
            scrutinized_asset = account_info['created-assets'][idx]
            idx = idx + 1       
            if (scrutinized_asset['index'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['index']))
                print(json.dumps(my_account_info['params'], indent=4))
                break
    
    #   Utility function used to print asset holding for account and assetid
    def print_asset_holding(algodclient, account, assetid):
        # note: if you have an indexer instance available it is easier to just use this
        # response = myindexer.accounts(asset_id = assetid)
        # then loop thru the accounts returned and match the account you are looking for
        account_info = algodclient.account_info(account)
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1        
            if (scrutinized_asset['asset-id'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                print(json.dumps(scrutinized_asset, indent=4))
                break
    
    print("Account 1 address: {}".format(pk))
    
    
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    

    txn = AssetConfigTxn(
        sender=pk,
        sp=params,
        index=asset_id, 
        note = meta_data.encode(),
        strict_empty_address_check=False)

    # Sign with secret key of creator
    stxn = txn.sign(sk)
    
    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(txid)
    
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client,txid)
    
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])No docu
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, pk, asset_id)
        print_asset_holding(algod_client, pk, asset_id)
    except Exception as e:
        print(e)

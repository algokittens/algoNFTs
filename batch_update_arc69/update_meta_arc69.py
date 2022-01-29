#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: algokittens
"""
import json
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future.transaction import AssetConfigTxn
import pandas as pd 
import os


def update_by_csv_file(csv_path, external_url, mnemonic1, description, testnet, update_all, row_to_update):
    df = pd.read_csv(csv_path)

    if (update_all==False):
        n=row_to_update-1 #run first line
        update_meta(n, csv_path, mnemonic1, external_url, description, testnet)
    else:
        for n in range(0,len(df)):
            update_meta(n, csv_path, mnemonic1, external_url, description, testnet)


def update_by_arc69_jsons(arc69_path, mnemonic1, testnet):
    for filename in os.listdir(arc69_path):
        if not filename.endswith(".json"): continue

        asset_id = filename.split('.')[0]

        with open(os.path.join(arc69_path,filename)) as file:
            arc69_data = json.load(file)
            meta_data = json.dumps(arc69_data)
            print(meta_data)
            send_algod_request(mnemonic1, asset_id, meta_data, testnet)


def update_meta(n, csv_path, mnemonic1, external_url, description, testnet=True):
    data_frame = pd.read_csv(csv_path)

    asset_id = data_frame['ID'][n]
    meta_data_json = get_meta_data_json(n, external_url, description, data_frame)
    print(meta_data_json)
    
    send_algod_request(mnemonic1, testnet, asset_id, meta_data_json)


def send_algod_request(mnemonic1, asset_id, meta_data_json, testnet=True):
    pk = mnemonic.to_public_key(mnemonic1)
    sk = mnemonic.to_private_key(mnemonic1)
    
    algod_address = "https://api.testnet.algoexplorer.io" if testnet else "https://api.algoexplorer.io"
    algod_token = ""
    headers = {'User-Agent': 'py-algorand-sdk'}
    algod_client = algod.AlgodClient(algod_token, algod_address, headers);    
    status = algod_client.status()

    print("Account 1 address: {}".format(pk))

    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    txn = AssetConfigTxn(
        sender=pk,
        sp=params,
        index=asset_id, 
        manager=pk,
        reserve=pk,
        freeze=pk,
        note = meta_data_json.encode(),
        strict_empty_address_check=False,
        clawback=None)

    # Sign with secret key of creator
    stxn = txn.sign(sk)

    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(txid)

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


def get_meta_data_json(n, external_url, description, data_frame):
    d = data_frame.drop(['ID'], axis=1)
    
    items = d.iloc[n]
    items = items[items != "None"]
    items = items.dropna()
    items = items.apply(str)
    properties = items.to_dict()

    meta_data = {
        "standard": "arc69",
        "description": description,
        "external_url": external_url,
        "properties": properties
    }

    # Remove keys with empty values
    meta_data = { key: value for key, value in meta_data.items() if value != '' }

    return json.dumps(meta_data)


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
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
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

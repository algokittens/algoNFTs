#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: algokittens
"""
import json
from algosdk.future.transaction import AssetConfigTxn
import pandas as pd 
import os, sys, inspect
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.algod_helper import wait_for_confirmation, print_created_asset, print_asset_holding

settings = Settings('batch_update_arc69')
pk = settings.get_public_key()
sk = settings.get_private_key()

def run_script():
    if settings.input_path.endswith('.csv'):
        update_by_csv_file()
    else:
        update_by_arc69_jsons()

def update_by_csv_file():
    df = pd.read_csv(settings.input_path)

    if (settings.csv['update_all'] == False):
        n = settings.csv['row_to_update'] -1 #run first line
        update_meta(n)
    else:
        for n in range(0,len(df)):
            update_meta(n)


def update_by_arc69_jsons():
    for filename in os.listdir(settings.input_path):
        if not filename.endswith(".json"): continue

        asset_id = filename.split('.')[0]

        with open(os.path.join(settings.input_path,filename)) as file:
            arc69_data = json.load(file)
            meta_data = json.dumps(arc69_data)
            print(meta_data)
            send_algod_request(asset_id, meta_data)


def update_meta(n):
    data_frame = pd.read_csv(settings.input_path)

    asset_id = data_frame['ID'][n]
    meta_data_json = get_meta_data_json(n, data_frame)
    print(meta_data_json)
    
    send_algod_request(asset_id, meta_data_json)


def send_algod_request(asset_id, meta_data_json):
    algod_client = settings.get_algod_client()

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


def get_meta_data_json(n, data_frame):
    d = data_frame.drop(['ID'], axis=1)
    
    items = d.iloc[n]
    items = items[items != "None"]
    items = items.dropna()
    items = items.apply(str)
    properties = items.to_dict()

    meta_data = {
        "standard": "arc69",
        "description": settings.csv['description'],
        "external_url": settings.csv['external_url'],
        "properties": properties
    }

    # Remove keys with empty values
    meta_data = { key: value for key, value in meta_data.items() if value != '' }

    return json.dumps(meta_data)


run_script()
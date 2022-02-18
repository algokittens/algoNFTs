#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 19:11:29 2021

@author: phyto
"""
from algosdk.future.transaction import AssetTransferTxn
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.algod_helper import wait_for_confirmation, print_asset_holding


settings = Settings('batch_add')
algod_client = settings.get_algod_client()
sk = settings.get_private_key()
pk = settings.get_public_key()


def add_asset(asset_id):
    asset_id = int(asset_id)
    
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
            print(f"asset {str(asset_id)} already added")
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


with open(settings.input_path) as csv_file:
    data = [line.rstrip() for line in csv_file]


for n in range(0, len(data)):
    add_asset(data[n])

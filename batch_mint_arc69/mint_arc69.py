# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:33:47 2021

@author: AlgoKittens
"""
import json
from algosdk import mnemonic
from algosdk.future.transaction import AssetConfigTxn
from algosdk.v2client import algod
import os, glob
import pandas as pd
from natsort import natsorted
import requests


def mint_asset (n, unit_name, asset_name, unit_name_number_digits, asset_name_number_digits, mnemonic1, image_path, meta_path, meta_type, api_key, api_secret, external_url, description, use_csv_asset_name, use_csv_cid, use_csv_description, testnet=True):
    if not use_csv_cid:
        ipfs_cid = get_cid_from_pinata(n, image_path, api_key, api_secret)

    if (meta_type=="csv"):
        d = pd.read_csv(meta_path)    
        items = d.iloc[n]
        items = items[items != "None"]
        items = items.dropna()
        items = items.apply(str)
        if use_csv_asset_name:
            csv_asset_name = items.pop('name')
        if use_csv_cid:
            csv_ipfs_url = items.pop('cid')
        if use_csv_description:
            description = items.pop('description')
        attributes =  items.to_dict()
    
    elif (meta_type=="JonBecker"):
        d = pd.read_json(meta_path)    
        d.drop('tokenId', axis=1, inplace=True)
        items = d.iloc[n]
        items = items[items != "None"]
        attributes = items.to_dict()
    
    elif (meta_type=="HashLips"):
        d = pd.read_json(meta_path)
        l = d['attributes'][n]
        records = pd.DataFrame.from_records(l).set_index('trait_type')
        attributes = records.iloc[:,0].to_dict()


    meta_data = {
        "standard": "arc69",
        "description": description,
        "external_url": external_url,
        "properties": attributes
    }

    # Remove keys with empty values
    meta_data = { key: value for key, value in meta_data.items() if value != '' }

    meta_data_json = json.dumps(meta_data)
            
    # an accounts dict.
    accounts = {}
    counter = 1
    for m in [mnemonic1]:
        accounts[counter] = {}
        accounts[counter]['pk'] = mnemonic.to_public_key(m)
        accounts[counter]['sk'] = mnemonic.to_private_key(m)
        counter += 1
    
    
    if (testnet==True):
        algod_address = "https://api.testnet.algoexplorer.io"
    elif (testnet==False):
        algod_address = "https://api.algoexplorer.io"
        
    algod_token = ""
    headers = {'User-Agent': 'py-algorand-sdk'}
    algod_client = algod.AlgodClient(algod_token, algod_address, headers);    
    status = algod_client.status()
    
    
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
        idx = 0
        for my_account_info in account_info['created-assets']:
            scrutinized_asset = account_info['created-assets'][idx]
            idx = idx + 1       
            if (scrutinized_asset['index'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['index']))
                print(json.dumps(my_account_info['params'], indent=4))
                break
    
    print("Account 1 address: {}".format(accounts[1]['pk']))
    
    
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    asset_number = str(n+1)
    asset_name = csv_asset_name if use_csv_asset_name else asset_name + asset_number.zfill(asset_name_number_digits)
    url = csv_ipfs_url if use_csv_cid else f"ipfs://${ipfs_cid}"

    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        total= 1,
        default_frozen=False,
        unit_name=unit_name + asset_number.zfill(unit_name_number_digits),
        asset_name=asset_name, 
        manager=accounts[1]['pk'],
        reserve=accounts[1]['pk'],
        freeze=None,
        clawback=None,
        strict_empty_address_check=False,
        url=url,
        metadata_hash= "", 
        note = meta_data_json.encode(),

        decimals=0)

    exit()
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]['sk'])
    
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
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)

def get_cid_from_pinata(n, image_path, api_key, api_secret):
    imgs = natsorted(glob.glob(os.path.join(image_path, "*.png")))
        
    files = [('file', (str(n)+".png", open(imgs[n], "rb"))),]
        
    headers = {        
            'pinata_api_key': api_key,
            'pinata_secret_api_key': api_secret    
        }   
        
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        
    response: requests.Response = requests.post(url=ipfs_url, files=files, headers=headers)
    meta = response.json()
        
    return meta['IpfsHash']

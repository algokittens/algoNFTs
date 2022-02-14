# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:33:47 2021

@author: AlgoKittens
"""
import json
from algosdk.future.transaction import AssetConfigTxn
import os, glob, sys, inspect
import pandas as pd
from natsort import natsorted
import requests
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.algod_helper import wait_for_confirmation, print_created_asset

settings = Settings('batch_mint_arc69')
pk = settings.get_public_key()
sk = settings.get_private_key()

def mint_asset(n):
    if not settings.use_csv_ipfs_url:
        pinata_ipfs_cid = get_cid_from_pinata(n, settings.image_path, settings.api_key, settings.api_secret)

    if (settings.meta_type == "csv"):
        d = pd.read_csv(settings.meta_path)    
        items = d.iloc[n]
        items = items[items != "None"]
        items = items.dropna()
        items = items.apply(str)
        # Handle csv data that shouldn't show up in arc69 properties
        if 'asset_id' in items: items.pop('asset_id')
        csv_asset_name = items.pop('asset_name') if 'asset_name' in items else ''
        csv_ipfs_url = items.pop('ipfs_url') if 'ipfs_url' in items else ''
        csv_description = items.pop('description') if 'description' in items else ''
        csv_external_url = items.pop('external_url') if 'external_url' in items else ''
        attributes =  items.to_dict()
    
    elif (settings.meta_type == "JonBecker"):
        d = pd.read_json(settings.meta_path)    
        d.drop('tokenId', axis=1, inplace=True)
        items = d.iloc[n]
        items = items[items != "None"]
        attributes = items.to_dict()
    
    elif (settings.meta_type == "HashLips"):
        d = pd.read_json(settings.meta_path)
        l = d['attributes'][n]
        records = pd.DataFrame.from_records(l).set_index('trait_type')
        attributes = records.iloc[:,0].to_dict()


    meta_data = {
        "standard": "arc69",
        "description": csv_description if settings.use_csv_description else settings.description,
        "external_url": csv_external_url if settings.use_csv_external_url else settings.external_url,
        "properties": attributes
    }

    # Remove keys with empty values
    meta_data = { key: value for key, value in meta_data.items() if value != '' }

    meta_data_json = json.dumps(meta_data)
            
    print("Account 1 address: {}".format(pk))
    
    algod_client = settings.get_algod_client()
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    asset_number = str(n+1)
    asset_name = csv_asset_name if settings.use_csv_asset_name else settings.asset_name + asset_number.zfill(settings.asset_name_number_digits)
    unit_name = settings.unit_name + asset_number.zfill(settings.unit_name_number_digits)
    url = csv_ipfs_url if settings.use_csv_ipfs_url else f"ipfs://{pinata_ipfs_cid}"

    txn = AssetConfigTxn(
        sender=pk,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name, 
        manager=pk,
        reserve=pk,
        freeze=None,
        clawback=None,
        strict_empty_address_check=False,
        url=url,
        metadata_hash= "", 
        note = meta_data_json.encode(),
        decimals=0)

    sign_and_send_txn(algod_client, txn)


def sign_and_send_txn(algod_client, txn):
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 02 21:21:39 2022

@author: grexn
"""
import base64
import os
import json
import csv
from algosdk.v2client import indexer


## USER SETTINGS ##
PUBLIC_KEY = "YOUR_PUBLIC_KEY"
OUTPUT_PATH = "./output_path/"
CSV_BASE_ATTRIBUTES = "description" #set ARC69 base attributes you want to add to csv e.g. "description,external_url" or "" for none
CSV_ADD_ASSET_NAME = True #Adds name of the asset to csv
CSV_ADD_IPFS_HASH = True #Adds cid column to csv
TESTNET = False
##################

INDEXER_ADDRESS = "https://testnet.algoexplorerapi.io/idx2" if TESTNET else "https://algoexplorerapi.io/idx2"
ALGOD_TOKEN = ""
HEADERS = {'User-Agent': 'py-algorand-sdk'}


myindexer = indexer.IndexerClient(indexer_token="", headers=HEADERS, indexer_address=INDEXER_ADDRESS)


def write_meta_data_to_files(indexer, public_key):
    created_assets = indexer.account_info(address=public_key)['account']['created-assets']
    data = []
    for asset in created_assets:
        asset_id = asset['index']
        is_deleted = asset['deleted']
        asset_name = asset['params']['name']
        ipfs_hash = asset['params']['url']
        last_config_tnx = myindexer.search_asset_transactions(asset_id,txn_type='acfg')['transactions'][-1]
        if 'note' in last_config_tnx and not is_deleted:
            print(f"ASA ID {asset_id}: metadata found - adding.")
            file_path = f"{OUTPUT_PATH}{asset_id}.json"
            check_and_create_path(file_path)
            with open(file_path, "w", encoding='utf-8') as json_file:
                json_string = base64.b64decode(last_config_tnx['note']).decode('utf-8')
                json_file.write(json_string)
                json_data_as_dict = json.loads(json_string)
                data.append((asset_id, asset_name, ipfs_hash, json_data_as_dict))
        else:
            print(f"ASA ID {asset_id}: no metadata found.")

    write_csv_file(data)


def write_csv_file(data):
    sortedData = sorted(data)

    converted_data = []
    attribute_keys = []
    arc69_base_attributes = CSV_BASE_ATTRIBUTES.split(',') if CSV_BASE_ATTRIBUTES else ''

    for asset_id, asset_name, ipfs_hash, asset in sortedData:
        new_asset = {}

        if CSV_ADD_ASSET_NAME and asset_name:
            new_asset['name'] = asset_name
            if 'name' not in attribute_keys:
                attribute_keys.append('name')


        if CSV_ADD_IPFS_HASH and ipfs_hash:
            new_asset['cid'] = ipfs_hash
            if 'cid' not in attribute_keys:
                attribute_keys.append('cid')

        if arc69_base_attributes:
            for base_attribute in arc69_base_attributes:
                new_asset[base_attribute] = asset[base_attribute]

        for attribute in asset['properties'].keys():
            new_asset[attribute] = asset['properties'][attribute]
        converted_data.append(new_asset)
        for attribute in new_asset:
            if attribute not in attribute_keys:
                attribute_keys.append(attribute)

    csv_file_path = f"{OUTPUT_PATH}metadata.csv"
    check_and_create_path(csv_file_path)
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f: 
        wr = csv.DictWriter(f, fieldnames = attribute_keys) 
        wr.writeheader()
        wr.writerows(converted_data) 


def check_and_create_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


write_meta_data_to_files(myindexer, PUBLIC_KEY)
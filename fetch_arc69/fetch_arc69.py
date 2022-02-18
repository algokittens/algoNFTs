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
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.file_helper import check_and_create_path


settings = Settings('fetch_arc69')
myindexer = settings.get_indexer()
OUTPUT_PATH = settings.get_output_folder()

def write_meta_data_to_files():
    account = myindexer.account_info(address=settings.public_key)['account']

    if not 'created-assets' in account:
        print(f"No assets found in account: {settings.public_key} and {'testnet' if settings.full_settings['testnet'] else 'mainnet'}")
        exit()

    created_assets = myindexer.account_info(address=settings.public_key)['account']['created-assets']
    #del created_assets[4:]
    data = []
    for asset in created_assets:
        asset_id = asset['index']
        is_deleted = asset['deleted']
        asset_name = asset['params']['name']
        ipfs_hash = asset['params']['url']
        last_config_tnx = myindexer.search_asset_transactions(asset_id,txn_type='acfg')['transactions'][-1]

        if 'note' in last_config_tnx and not is_deleted:
            print(f"ASA ID {asset_id}: metadata found - adding.")
            file_path = f"{OUTPUT_PATH}/{asset_id}.json"
            check_and_create_path(file_path)
            with open(file_path, "w", encoding='utf-8') as json_file:
                json_string = base64.b64decode(last_config_tnx['note']).decode('utf-8')
                json_file.write(json_string)
                json_data_as_dict = json.loads(json_string)
                data.append((asset_id, asset_name, ipfs_hash, json_data_as_dict))
        else:
            print(f"ASA ID {asset_id}: no metadata found.")

    print(f"Total assets added: {len(data)}")
    write_csv_file(data)


def write_csv_file(data):
    sortedData = sorted(data)

    converted_data = []
    csv_header = []

    for asset_id, asset_name, ipfs_hash, asset in sortedData:
        new_asset = {}

        if settings.csv['add_asset_id'] and asset_id:
            new_asset['asset_id'] = asset_id

        if settings.csv['add_asset_name'] and asset_name:
            new_asset['asset_name'] = asset_name

        if settings.csv['add_ipfs_url'] and ipfs_hash:
            new_asset['ipfs_url'] = ipfs_hash

        base_attributes = settings.csv['base_attributes']
        if base_attributes:
            for base_attribute in settings.csv['base_attributes'].split(','):
                new_asset[base_attribute] = asset[base_attribute]

        for attribute in asset['properties'].keys():
            new_asset[attribute] = asset['properties'][attribute]
        
        converted_data.append(new_asset)

        for attribute in new_asset:
            if attribute not in csv_header:
                csv_header.append(attribute)

    csv_file_path = f"{OUTPUT_PATH}/metadata.csv"
    check_and_create_path(csv_file_path)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f: 
        wr = csv.DictWriter(f, fieldnames = csv_header) 
        wr.writeheader()
        wr.writerows(converted_data)

    print(f"Script complete - output can be found here: {OUTPUT_PATH}")


write_meta_data_to_files()
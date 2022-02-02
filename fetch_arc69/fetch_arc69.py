#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 02 21:21:39 2022

@author: grexn
"""
import base64
import os
from algosdk.v2client import indexer


## USER SETTINGS ##
PUBLIC_KEY = "YOUR_PUBLIC_KEY"
OUTPUT_PATH = "./your_folder/"
TESTNET = False
##################

INDEXER_ADDRESS = "https://testnet.algoexplorerapi.io/idx2" if TESTNET else "https://algoexplorerapi.io/idx2"
ALGOD_TOKEN = ""
HEADERS = {'User-Agent': 'py-algorand-sdk'}


myindexer = indexer.IndexerClient(indexer_token="", headers=HEADERS, indexer_address=INDEXER_ADDRESS)


def writeMetaDataToFiles(indexer, public_key):
    created_assets = indexer.account_info(address=public_key)['account']['created-assets']
    for asset in created_assets:
        asset_id = asset['index']
        is_deleted = asset['deleted']
        last_config_tnx = myindexer.search_asset_transactions(asset_id,txn_type='acfg')['transactions'][-1]
        if 'note' in last_config_tnx and not is_deleted:
            file_path = f"{OUTPUT_PATH}{asset_id}.json"
            checkAndCreatePath(file_path)
            with open(file_path, "w", encoding='utf-8') as json_file:
                json_file.write(base64.b64decode(last_config_tnx['note']).decode('utf-8'))


def checkAndCreatePath(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


writeMetaDataToFiles(myindexer, PUBLIC_KEY)
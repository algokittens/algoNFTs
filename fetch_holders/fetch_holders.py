#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 13:21:39 2021

@author: algokittens
"""
import pandas as pd
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings
from lib.file_helper import check_and_create_path
from datetime import date,datetime

settings = Settings('fetch_holders')
myindexer = settings.get_indexer()
OUTPUT_PATH = settings.get_output_folder()

response = myindexer.account_info(address=settings.public_key)

if not 'created-assets' in response['account']:
    print(f"No assets found in account: {settings.public_key} and {'testnet' if settings.full_settings['testnet'] else 'mainnet'}")
    exit()

created_assets = response['account']['created-assets']

def fetch_account(asset_id):
    response = myindexer.asset_balances(asset_id)
    df = pd.DataFrame(response['balances'])
    df['asset_id'] = asset_id
    d = df.loc[(df.amount == 1)]
    return(d)


addresses = []
for asset in created_assets:
    addresses.append(fetch_account(asset['index']))


data = pd.concat(addresses, axis=0)
data = data[['asset_id', 'address']]
out_file = f"{OUTPUT_PATH}/{settings.public_key[0:5]}_holders_{date.isoformat(datetime.now())}.csv"
check_and_create_path(out_file)

data.to_csv(out_file, index=False)

print(f'Holders saved to: {os.path.abspath(out_file)}')

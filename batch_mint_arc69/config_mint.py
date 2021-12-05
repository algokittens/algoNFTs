#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 23:07:24 2021

@author: AlgoKittens
"""

from mint_arc69 import mint_asset
import pandas as pd 

testnet= True

meta_path = "/media/phyto/1TB_HD/Batchguide/example_NFT.csv" #location of metadata
image_path = "/media/phyto/1TB_HD/Batchguide/images" #location of images
unit_name = "TST"
asset_name = "Test NFT #"
algod_token = "" #your purestake api token goes here
api_key = "" #your pinata key
api_secret = "" #your pinata secret
mnemonic1 = ""
external_url = ""
description = ""


df = pd.read_csv(meta_path)    
for n in range(0,len(df)):
    mint_asset (n, unit_name, asset_name, mnemonic1, image_path, meta_path, algod_token, api_key, api_secret, external_url, description, testnet=testnet)

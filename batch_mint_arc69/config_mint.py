#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 23:07:24 2021

@author: AlgoKittens
"""

from mint_arc69 import mint_asset
import pandas as pd 
from pathlib import Path


testnet= True

meta_path = Path("e:/Repositories/algoNFTs/batch_mint_arc69/example.csv") #location of metadata
meta_type = "csv" #metadata type, valid argments = "csv", "JonBecker", "HashLips"
image_path = Path("/media/phyto/1TB_HD/Batchguide/images") #location of images
unit_name = "TST"
asset_name = "Test NFT #"
unit_name_number_digits = 0 #set number of digits for unit_name e.g. 4 will result in: TST0001 or TST0999 - leave at zero to increment without leading zero(s)
asset_name_number_digits = 0 #set number of digits for asset_name e.g. 4 will result in: Test NFT #0001 or Test NFT #0999 - leave at zero to increment without leading zero(s)
api_key = "" #your pinata key
api_secret = "" #your pinata secret
mnemonic1 = ""
external_url = ""
description = ""
use_csv_description = True #set to true if you have a "description" column in your csv that should be used as meta arc69 description

if (meta_type=="csv"):
    df = pd.read_csv(meta_path)    

elif (meta_type=="JonBecker"):
    df = pd.read_json(meta_path)    

elif (meta_type=="HashLips"):
    df = pd.read_json(meta_path)    
    
for n in range(0,len(df)):
    mint_asset (n, unit_name, asset_name, unit_name_number_digits, asset_name_number_digits, mnemonic1, image_path, meta_path, meta_type, api_key, api_secret, external_url, description, use_csv_description, testnet=testnet)

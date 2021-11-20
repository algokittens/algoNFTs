#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:50:42 2021

@author: algokittens
"""

import pandas as pd 
from update_meta_arc69 import update_meta


csv_path = "/home/phyto/example_NFT.csv"
external_url = "yourwebsite.com"
algod_token = "" #called YOUR API Key on Purestake
mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens"
description = "some cool description"
#description = ""


testnet=True
update_all = False #if true updates every NFT in the csv
row_to_update = 1 #update only the asset in the first row of the csv


df = pd.read_csv(csv_path)    

if(update_all==False):
    n=row_to_update-1 #run first line
    update_meta(n, csv_path, mnemonic1, external_url, description, algod_token, testnet)
    
else:
    for n in range(0,len(df)):
        update_meta(n, csv_path, mnemonic1, external_url, description,  algod_token, testnet)

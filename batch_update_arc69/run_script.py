#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:50:42 2021

@author: algokittens
"""

import pandas as pd 
from update_meta_arc69 import update_by_csv_file
from update_meta_arc69 import update_by_arc69_jsons
import os

current_dirname = os.path.dirname(__file__)

# if arc69_path is not path to csv File script will handle it as folder with arc69 json files
arc69_path = os.path.join(current_dirname, './example_NFT.csv')

external_url = "yourwebsite.com"
description = "some cool description"

mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens"

testnet=True
update_all = False #if true updates every NFT in the csv
row_to_update = 1 #update only the asset in the first row of the csv


if arc69_path.endswith('.csv'):
    update_by_csv_file(arc69_path, external_url, mnemonic1, description, testnet, update_all, row_to_update)
else:
    update_by_arc69_jsons(arc69_path, mnemonic1, testnet)

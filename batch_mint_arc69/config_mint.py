#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 23:07:24 2021

@author: AlgoKittens
"""

from mint_arc69 import mint_asset
import pandas as pd 
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from lib.settings import Settings


settings = Settings('batch_mint_arc69')

if (settings.meta_type == "csv"):
    df = pd.read_csv(settings.meta_path)   

elif (settings.meta_type == "JonBecker"):
    df = pd.read_json(settings.meta_path)    

elif (settings.meta_type == "HashLips"):
    df = pd.read_json(settings.meta_path)

for n in range(0,len(df)):
    mint_asset (n)

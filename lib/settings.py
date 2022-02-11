import yaml
from pathlib import Path
import os
from algosdk.v2client import indexer


class Settings:

    full_settings = {}
    indexer_address = ''

    def __init__(self, settings_key):
        self.settings_key = settings_key
        module_path = os.path.dirname(__file__)
        settings_path = os.path.join(module_path, '../settings.yaml')
        with open(settings_path, 'r') as file:
            self.full_settings = yaml.safe_load(file)
        
        if self.full_settings['testnet']:
            self.indexer_address = self.full_settings['indexer_address']['testnet']
        else:
            self.indexer_address = self.full_settings['indexer_address']['mainnet']
        self.context_settings = self.full_settings[self.settings_key]
    
    def get_indexer(self):
        indexer_address = self.indexer_address
        headers = {'User-Agent': 'py-algorand-sdk'}
        return indexer.IndexerClient(indexer_token="", headers=headers, indexer_address=indexer_address)


    def __getattr__(self, name):
        return self.context_settings[name]


    def get_output_folder(self):
        root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
        return os.path.join(root_path, self.full_settings['default_output_folder'], self.settings_key)

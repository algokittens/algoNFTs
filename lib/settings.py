import yaml
import os
from algosdk.v2client import indexer, algod
from algosdk import mnemonic

class Settings:
    INDEXER_ADDRESSES = {
        "testnet": "https://testnet.algoexplorerapi.io/idx2",
        "mainnet": "https://algoexplorerapi.io/idx2"
    }
    ALGOD_ADDRESSES = {
        "testnet": "https://api.testnet.algoexplorer.io",
        "mainnet": "https://api.algoexplorer.io"
    }

    full_settings = {}

    def __init__(self, settings_key):
        self.settings_key = settings_key
        module_path = os.path.dirname(__file__)
        settings_path = os.path.join(module_path, '../settings.yaml')
        with open(settings_path, 'r') as file:
            self.full_settings = yaml.safe_load(file)
        
        if self.full_settings['testnet']:
            self.indexer_address = self.INDEXER_ADDRESSES['testnet']
            self.algod_address = self.ALGOD_ADDRESSES['testnet']
        else:
            self.indexer_address = self.INDEXER_ADDRESSES['mainnet']
            self.algod_address = self.ALGOD_ADDRESSES['mainnet']
        self.context_settings = self.full_settings[self.settings_key]
    
    def get_indexer(self):
        indexer_address = self.indexer_address
        headers = {'User-Agent': 'py-algorand-sdk'}
        return indexer.IndexerClient(indexer_token="", headers=headers, indexer_address=indexer_address)

    def get_algod_client(self):
        indexer_address = self.algod_address
        headers = {'User-Agent': 'py-algorand-sdk'}
        return algod.AlgodClient(algod_token="", algod_address=indexer_address, headers=headers);    

    def __getattr__(self, name):
        return self.context_settings[name]


    def get_output_folder(self):
        root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
        return os.path.join(root_path, self.full_settings['default_output_folder'], self.settings_key)

    def get_private_key(self):
        pass_phrase = self.context_settings['mnemonic1']
        return mnemonic.to_private_key(pass_phrase.replace(',', ''))
    
    def get_public_key(self):
        pass_phrase = self.context_settings['mnemonic1']
        return mnemonic.to_public_key(pass_phrase.replace(',', ''))


import yaml
from pathlib import Path
import os



class Settings:

    def __init__(self):
        module_path = os.path.dirname(__file__)
        settings_path = os.path.join(module_path, '../settings.yaml')
        with open(settings_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        self.data = yaml_data



    def get_indexer_address(self):
        return self.data['indexer_address']['testnet'] if self.data['testnet'] else self.data['indexer_address']['mainnet']


indexer_addres = Settings().get_indexer_address()

was = 'WAS'
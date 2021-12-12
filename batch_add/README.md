# Batch adding NFTs using python

# Pre-requirements
This pipeline requires two dependencies which have to be installed prior to running.

AlgoSDK which can be installed using [PIP](https://pypi.org/) , by opening your terminal and running the following:

```pip3 install py-algorand-sdk```

and dotenv which can be installed using PIP, by opening the terminal and running the following:

```pip3 install python-dotenv```


# Preparing the script

## Create .env file

For this pipeline all env data should be defined in an .env file which will then be loaded into the main script when running.


```
# .env
testnet=True
asset_ids = "/media/phyto/1TB_HD/batch_add/example_add.csv"
m = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens"
```

This file can be prepared using notepad or a similair applications which should be named `.env` and be stored in the same folder as `add_asset.py`


### a) Testnet

This variable should define if the testnet is to be used.
For mainnet: `testnet=False`

### b) asset_ids

This variable should point to the csv containing the assets to be added. It should contain no header and only the asset IDs to be added

### c) asset_ids

This is your algorand key. Included below is a testnet account containing no real algos. In reality this should not be shared with ANYONE.

```mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens"```


# Running the script

Once you have defined your `.env` file, run the script from the terminal or using your favourite IDE (open file + F5 in Spyder).

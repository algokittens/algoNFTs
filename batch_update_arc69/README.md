
# How to batch update your existing ASAs to ARC69 using python

# Pre-requirements
This guide will walk you through batch updating NFTs on Algorand to [ARC69](https://github.com/algokittens/arc69) using Python. No prior experience with Python is assumed, but you will be required to make some changes to the Python script to suit your requirements.
This pipeline should only be ran on a secure machine, and we recommend checking out the official algorand documentation beforehand: https://developer.algorand.org/docs/get-details/asa/

Please note that I write these guides and scripts in my spare time and they come with no warranty of any kind whatsoever.  

# Download & Installation

Make sure you downloaded the whole repository and followed the steps in the main [readme](../README.md).

# Prepare your data
## Option A:
The data format for this pipeline is csv, which can be generated from excel files by exporting to "comma separated values".

For the spreadsheet, only the traits should be included as well as a column called 'ID' which should contain the ASA ID. None values should be called ```None```.

## Option B:
Put your complete ARC69 metadata files in a folder. The metadata must be filled in according to the definition (see [example_data](example_data/arc69_data/)). 

One of these two formats **MUST** be followed otherwise the script will not work. 


# Running the script

For this example we will update three example NFTs: 43432985, 43432860, and 43432496, which were minted on the testnet using the mnemonic included. It is strongly recommended to experiment with these assets before moving to the mainnet and spending real algos.

The csv file can be found in the github directory and is entitled: "example_NFT.csv".

## 1) Open settings.yaml

Using Spyder (or your favourite IDE) open your `settings.yaml`. All changes should be made within this file rather than update_meta_arc69.py unless you need to add some additional specifications.

## 2) Edit settings.yaml
These are the settings to adjust for this script to run properly:

```
batch_update_arc69:
    mnemonic1: "wreck floor carbon during ..."
    input_path: "e:/algoNFTs/batch_update_arc69/example_data/example_NFT.csv"
    # Settings relevant for csv input_path ONLY! (Option A)
    csv:
        external_url: "yourwebsite.com"
        description: "some cool description"
        update_all: true #if true updates every NFT in the csv
        row_to_update: 1 #update only the asset in the first row of the csv
```
### a) Define your mnemonic 
This is your algorand key. Included below is access to a testnet account containing no real algos. In reality this should not be shared with ANYONE.

```mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens" ```

### b) Add the path of your csv containing your metadata.

``` input_path = r"C:/Users/AlgoKittens/example_NFT.csv" ```

### c) Define the description ([Option A](#option-a) only)
This description will be included in every asset. If left blank, no description will be included:

``` description = "your awesome description goes here"```

### d) Define the external URL ([Option A](#option-a) only)
This url will be included in every asset. If left blank, no URL will be included:

``` external_url = "your_website.com"```

### e) Define items to update ([Option A](#option-a) only)
Define if every NFT in the spreadsheet should be updated. If set to true, all assets will be updated.
```update_all = False```

If you only want to update a single row, define which row should be updated:

```row_to_update = 1 # this would update row 1```

### f) Notes for preparation with [Option B](#option-b)
`external_url` and `description` will be ignored since your ARC69 files are considered complete.

`update_all` and `row_to_update` will also be ignored. In case files shouldn't be used for update, they should be moved temporarily in a different directory.


## 3) Run the script

Once all the desired changes are made run the script (play icon or F5 if you are using Spyder).


### View your NFT

After updating your NFTs they can can be viewed on randgallery. Note that if you minted your NFT on the tesnet, you need the '&testnet’ flag at the end of the NFT to view.

Example NFT 1:
https://www.randgallery.com/algo-collection/?address=43432496&testnet

Example NFT 2:
https://www.randgallery.com/algo-collection/?address=43432860&testnet

Example NFT 3:
https://www.randgallery.com/algo-collection/?address=43432985&testnet



## 4) Common problems:

### a) Packages not loading/recognized:

If you did not install Python, Spyder, or the dependencies using anaconda, you might see error messages that the packages could not be loaded. In such a scenario it is recommended to uninstall everything, and reinstall ONLY using anaconda.

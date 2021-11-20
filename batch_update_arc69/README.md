
# How to batch update your existing ASAs to ARC69 using python

# Pre-requirements
This guide will walk you through batch updating NFTs on Algorand to [ARC69](https://github.com/algokittens/arc69) using Python. No prior experience with Python is assumed, but you will be required to make some changes to the Python script to suit your requirements.
This pipeline should only be ran on a secure machine, and we recommend checking out the official algorand documentation beforehand: https://developer.algorand.org/docs/get-details/asa/

Please note that I write these guides and scripts in my spare time and they come with no warranty of any kind whatsoever.  

## 1) Purestake account

Go to https://developer.purestake.io/ and sign up for a free account. Once registered you will be directed to a homepage containing an algod token titled "YOUR API KEY".
You will need this key to connect to the algorand network later in this guide.

## 2) Install Python

If you do not already have Python installed, install python using Anaconda: https://www.anaconda.com/products/individual. Installing just Miniconda is fine as we will not need the other packages.

## 3) Install Python IDE
We will use a Python IDE to update and run the scripts. In this guide we will use https://www.spyder-ide.org/, although if you develop in multiple languages https://code.visualstudio.com/ is a great alternative. 

## 4) Install Python dependencies

This pipeline requires two dependencies which have to be installed prior to running.

AlgoSDK which can be installed using PIP, but opening up your terminal and running the following:

```pip3 install py-algorand-sdk```

and Pandas which can be installed using Anaconda, by opening up the anaconda terminal and running the following:

```conda install pandas```


## 5) Prepare your data

The data format for this pipeline is csv, which can be generated from excel files by exporting to "comma separated values".

For the spreadsheet, only the traits should be included as well as a column called 'ID' which should contain the ASA ID. None values should be called 'None'.

This format **MUST** be followed otherwise the script will not work. 


# Running the script

For this example we will update three example NFTs: 43432985, 43432860, and 43432496, which were minted on the testnet using the mnemonic included. It is strongly recommended to experiment with these assets before moving to the mainnet and spending real algos.

The csv file can be found in the github directory and is entitled: "example_NFT.csv".

## 1) Download "run_script.py" and "update_meta_arc69.py"

Download both scripts and make sure that they are in the same folder. It very important that they are in same folder as otherwise the script will not work.

## 2) Open "run_script.py"

Using Spyder (or your favourite IDE) open "run_script.py". All changes should be made within this script rather than update_meta_arc69 unless you need to add some additional specifications

## 2) Edit "run_script.py"

### a) Add the path of your csv containing your metadata.

``` image_path = r"C:/Users/AlgoKittens/example_NFT.csv" ```

### b) Define the description.
This description will be included in every asset. If left blank, no URL will be included:

``` description = "your awesome description goes here"```

### c) Define the external URL.
This url will be included in every asset. If left blank, no URL will be included:

``` external_url = "your_website.com"```


### d) Define your algod token
This is called "YOUR API KEY" on Purestake.

``` algod_token = " " ```


### e) Define your mnemonic 
This is your algorand key. Included below is access to a testnet account containing no real algos. In reality this should not be shared with ANYONE.

```mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens" ```

### f) Define testnet or mainnet
The default is testnet. If you want to update on the mainnet set this to False:

```testnet = True```

### f) Define items to update

Define if every NFT in the spreadsheet should be updated. If set to true, all assets will be updated.
```update_all = False```

If you only want to update a single row, define which row should be updated:

```row_to_update = 1 # this would update row 1```


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



## 4) Known issues:


### a) Purestake rate limiting:

```AlgodHTTPError: Limit Exceeded```

Purestake will limit your access after updating around 500 assets. You can either wait 24 hours or make another account using a different email address.

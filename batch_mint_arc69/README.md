# How to batch mint algoNFTs following the ARC69 metadata standard using python

# Pre-requirements
This guide will walk you through batch minting NFTs on Algorand following [ARC69](https://github.com/algokittens/arc69) using Python. No prior experience with Python is assumed, but you will be required to make some changes to the Python script to suit your requirements.
This pipeline should only be ran on a secure machine, and we recommend checking out the official algorand documentation beforehand: https://developer.algorand.org/docs/get-details/asa/

Please note that I write these guides and scripts in my spare time and they come with no warranty of any kind whatsoever.  

## 1) Purestake account (connecting to algorand network)

Go to https://developer.purestake.io/ and sign up for a free account. Once registered you will be directed to a homepage containing an algod token titled "YOUR API KEY".
You will need this key to connect to the algorand network later in this guide.

## 2) Pinata account (connecting to ipfs)

Go to https://www.pinata.cloud/ and sign up for a free account. Once logged in go to "YOUR API KEYS" and then "create a new key", enable admin rights, and provide an appropriate key name, and create. Copy your keys in a secure location as it will only be provided once. You will need "API KEY" and "API Secret" later in this guide.


## 3) Install Python

If you do not already have Python installed, install python using Anaconda: https://www.anaconda.com/products/individual. Installing just Miniconda is fine as we will not need the other packages. 

## 4) Install Python IDE
We will use a Python IDE to update and run the scripts. Although if you develop in multiple languages https://code.visualstudio.com/ is a great alternative. 
Spyder can be installed by opening the anaconda terminal and running the following:

```conda install spyder```


## 4) Install Python dependencies

This pipeline requires three dependencies which have to be installed prior to running.

AlgoSDK which can be installed using [PIP](https://pypi.org/) , by opening your terminal and running the following:

```pip3 install py-algorand-sdk```

AlgoSDK which can be installed using PIP by opening your terminal and running the following:

```pip3 install natsort```



Pandas which can be installed using Anaconda, by opening the anaconda terminal and running the following:

```conda install pandas```


## 5) Prepare your data

The data format for this pipeline is csv, which can be generated from excel files by exporting to "comma separated values".

For the spreadsheet, only the traits should be included and the row should correlate to the file number (for example the metadata for 1.png should be in the first row). None values should be called ```None```.

Additionally apostrophes ```'```, should be avoided. For example instead of: ```good mornin'```, the format: ```good morning``` should be used. 

This format **MUST** be followed otherwise the script will not work. 


# Running the script

## 1) Download "config_mint.py" and "mint_arc69.py"

Download both scripts and make sure that they are in the same folder. It very important that they are in same folder as otherwise the script will not work.

## 2) Open "config_mint.py"

Using Spyder (or your favourite IDE) open "config_mint.py". All changes should be made within this script rather than mint_arc69.py unless you need to add some additional specifications.

## 2) Edit "config_mint.py"

### a) Define if Testnet should be used
The default configuration will use the testnet:

``` Testnet = True ```

Testnet algos can be acquired here: https://bank.testnet.algorand.network/

If you want to mint on the mainnet change it to:

``` Testnet = False ```


### b) Add the path of your csv containing your metadata.

``` meta_path = r"C:/Users/AlgoKittens/example_NFT.csv" ```


### c) Add the path of your folder containing your images.

``` image_path = r"C:/Users/AlgoKittens/my_images" ```


### c) Define the unit name.
This unit name will be applied to every NFT following the format unit_name + row number (e.g. TST1, TST2 etc.). The unit name **MUST** be 8 characters or less including the numbers. For example, if you plan to mint 999 assets, the max unit name is 5 characters.

``` unit_name = "TST" ```

### d) Define the asset name.

This asset name will be applied to every NFT following the format asset_name + row number (e.g. Test #1, Test #2 etc.).

``` asset_name = "Test NFT #" ```

### e) Define your PURESTAKE API key
This is called "YOUR API KEY" on Purestake.

``` algod_token = "" ```


### f) Define your Pinata API key

``` api_key = "" ```

### g) Define your Pinata Secret key

``` api_secret = "" ```


### h) Define your mnemonic 
This is your algorand key. Included below is access to a testnet account containing no real algos. In reality this should not be shared with ANYONE.

```mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens" ```

### i) Define the external URL.
This url will be included in every asset. If left blank, no URL will be included:

``` external_url = "your_website.com"```


### j) Define the description.
This url will be included in every asset. If left blank, no description will be included:

``` description = "your awesome description goes here"```


### j) Define which NFTs of the csv should be minted
To mint every NFT in the csv:

``` for n in range(0,len(df)): ```


To mint just the first NFT in the csv:

``` for n in range(0,1): ```


To mint from the 50th NFT in the csv onwards:

``` for n in range(49, len(df)): ```


## 3) Run the script

Once all the desired changes are made run the script (play icon or F5 if you are using Spyder).


### View your NFT

After updating your NFTs they can can be viewed on randgallery. Note that if you minted your NFT on the tesnet, you need the '&testnet’ flag at the end of the NFT to view.

Example NFT 1:
https://www.randgallery.com/algo-collection/?address=43432860&testnet



## 4) Common problems:

### a) Purestake rate limiting:

```AlgodHTTPError: Limit Exceeded```

Purestake will limit your access after updating around 500 assets. You can either wait 24 hours or make another account using a different email address.

### b) Packages not loading/recognized:

If you did not install Python, Spyder, or the dependencies using anaconda, you might see error messages that the packages could not be loaded. In such a scenario it is recommended to uninstall everything, and reinstall ONLY using anaconda.

# Batch minting algoNFTs following the ARC69 metadata standard using Python

# Pre-requirements
This guide will walk you through batch minting NFTs on Algorand following [ARC69](https://github.com/algokittens/arc69) using Python. No prior experience with Python is assumed, but you will be required to make some changes to the Python script to suit your requirements.
This pipeline should only be ran on a secure machine, and we recommend checking out the official algorand documentation beforehand: https://developer.algorand.org/docs/get-details/asa/

Please note that I write these guides and scripts in my spare time and they come with no warranty of any kind whatsoever.  

## 1) Pinata account (connecting to ipfs)

Go to https://www.pinata.cloud/ and sign up for a free account. Once logged in go to "YOUR API KEYS" and then "create a new key", enable admin rights, and provide an appropriate key name, and create. Copy your keys in a secure location as it will only be provided once. You will need "API KEY" and "API Secret" later in this guide.

## 2) Prepare your data

If you used the Jon Becker or HashLips tools to generate your images there is no further need to adjust the metadata and you can skip to the next section.

If you are using a spreadsheet, the metadata should first be exported as a csv (comma separated values) file. For the spreadsheet only the trait names and trait data should be included. The first row (the header row) should contain the trait names, and the other rows should correlate to the file number (for example the metadata for 1.png should be in the first non-header row - i.e. row 2 in Excel). None values should be empty or called ```None```. For an example see the [example csv.](https://github.com/algokittens/algoNFTs/blob/master/batch_mint_arc69/example.csv)

This format **MUST** be followed otherwise the script will not work. 


# Download & Installation

Make sure you downloaded the whole repository and followed the steps in the main [readme](../README.md).


# Adjust settings.yaml

Using Spyder (or your favourite IDE) open "settings.yaml". All changes should be made within this file rather than mint_arc69.py unless you need to add some additional specifications.


## 1) Add the path of your csv containing your metadata.

``` meta_path = r"C:/Users/AlgoKittens/example_NFT.csv" ```

## 2) Add the metadata type.

This should be either "JonBecker", "HashLips", or "csv"

``` meta_type = "csv" ```

## 3) Add the path of your folder containing your images.

``` image_path = r"C:/Users/AlgoKittens/my_images" ```


## 4) Define the unit name.
This unit name will be applied to every NFT following the format unit_name + row number (e.g. TST1, TST2 etc.). The unit name **MUST** be 8 characters or less including the numbers. For example, if you plan to mint 999 assets, the max unit name is 5 characters.

``` unit_name = "TST" ```

## 5) Define the asset name.

This asset name will be applied to every NFT following the format asset_name + row number (e.g. Test #1, Test #2 etc.).

``` asset_name = "Test NFT #" ```

## 6) Define your Pinata API key

``` api_key = "" ```

## 7) Define your Pinata Secret key

``` api_secret = "" ```


## 8) Define your mnemonic 
This is your algorand key. Included below is access to a testnet account containing no real algos. In reality this should not be shared with ANYONE.

```mnemonic1 = "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens" ```

## 9) Define the external URL.
This url will be included in every asset. If left blank, no URL will be included:

``` external_url = "your_website.com"```


## 10) Define the description.
This url will be included in every asset. If left blank, no description will be included:

``` description = "your awesome description goes here"```


## 11) Define which NFTs of the csv should be minted
This still needs to be setup in `config_mint.py`. To mint every NFT in the csv:

``` for n in range(0,len(df)): ```


To mint just the first NFT in the csv:

``` for n in range(0,1): ```


To mint from the 50th NFT in the csv onwards:

``` for n in range(49, len(df)): ```


# Run the script

Once all the desired changes are made run `config_mint.py` (play icon or F5 if you are using Spyder).


### View your NFT

After updating your NFTs they can can be viewed on randgallery. Note that if you minted your NFT on the tesnet, you need the '&testnet’ flag at the end of the NFT to view.

Example NFT 1:
https://www.randgallery.com/algo-collection/?address=43432860&testnet



# Common problems:

## 1) Packages not loading/recognized:

If you did not install Python, Spyder, or the dependencies using anaconda, you might see error messages that the packages could not be loaded. In such a scenario it is recommended to uninstall everything, and reinstall ONLY using anaconda.

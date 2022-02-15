# Fetching all Assets of an account with ARC69 data

# Overview
This script will fetch metadata of assets created by a provided creator address. Data for each asset will be saved as json where the filename corresponds to the ASA ID. Additionally the data will be saved as csv which can be used for [batch_mint_arc69](../batch_mint_arc69).



# Download & Installation

Make sure you downloaded the whole repository and followed the steps in the main [readme](../README.md).

# Adjust settings.yaml

Using Spyder (or your favourite IDE) open "settings.yaml". All changes should be made within this file unless you need to add some additional specifications.

```
fetch_arc69:
    public_key: "KKBVJLXALCENRXQNEZC44F4NQWGIEFKKIHLDQNBGDHIM73F44LAN7IAE5Q"
    csv:
        add_asset_id: false
        add_asset_name: false
        add_ipfs_url: false
        base_attributes: "description,external_url" 
```


## a) Define public key

``` public_key = "GANGAAWKBJBWQJIIETTLWQT7ZFGPC4UDIITNGP55BCQPB26IEMOPOHQMEA" ```


## b) Define additional csv data
With this setting you can add ARC69 base attributes to the csv export - **ONLY** add them if they are present in your json metadata. Leave empty if you want just the ARC69 properties to be added to the csv.

```base_attributes = "description"```

or mulitple with comma seperation

```base_attributes = "standard,description,external_url"```

also asset id, CID (ipfs hash) and asset name can be added to csv output:

```add_asset_id: true```


```add_asset_name: true```


```add_ipfs_url: true```



# Running the script

Once you have defined your parameters in the file, run the script from the terminal or using your favourite IDE (open file + F5 in Spyder).




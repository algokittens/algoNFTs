# Fetching all Assets of an account with ARC69 data

# Overview
This script will fetch metadata of assets created by a provided creator address. Data for each asset will be saved as json where the filename corresponds to the ASA ID.

This pipeline requires one dependencies which has to be installed prior to running.

AlgoSDK which can be installed using [PIP](https://pypi.org/), by opening your terminal and running the following:

```pip3 install py-algorand-sdk```

# Preparing the script

## a) Define public key

``` PUBLIC_KEY = "GANGAAWKBJBWQJIIETTLWQT7ZFGPC4UDIITNGP55BCQPB26IEMOPOHQMEA" ```


## b) Define were the files should be saved

```OUTPUT_PATH = "/home/algokittens/GANG_holders.csv"```



## c) Define if the testnet should be used

```TESTNET = False ```


# Running the script

Once you have defined your parameters in the file, run the script from the terminal or using your favourite IDE (open file + F5 in Spyder).




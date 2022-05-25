# Overview

# Intro
This repository provides guides and scripts to batch mint, transfer and update Algorand NFTs using Python. 
All these scripts and guides are written in my spare time and come with no warranty whatsoever of any kind.
Always run things on the testnet first, and it is strongly recommended to refer to the official Algorand documentations beforehand: https://developer.algorand.org/docs/features/asa/

## Available:
### a) Batch minting NFTs following ARC69
### b) Batch updating existing NFTs to ARC69
### c) Batch opt-into ASAs
### d) Fetch all holders of assets created by given address
### e) Fetch all asset information from an account as json or csv
### f) Batch opt-out ASAs with zero balance

## In Progress:
### a) Batch transfer ASAs

## Other resources:
### a) Random NFT art generator using Python:
https://github.com/Jon-Becker/nft-generator-py

### b) Random NFT art generator using JavaScript:
https://github.com/HashLips/hashlips_art_engine

# Pre-Requirements

## 1) Install Python

If you do not already have Python installed, install python using Anaconda: https://www.anaconda.com/products/individual. Installing just Miniconda is fine as we will not need the other packages. Alternatively if you're going to use Visual Studio Code (see next step), downloading and installing python from https://www.python.org/downloads/ is also possible.

## 2) Install Python IDE
We will use a Python IDE to update and run the scripts. Although if you develop in multiple languages https://code.visualstudio.com/ is a great alternative. 
Spyder can be installed by opening the anaconda terminal and running the following:

```conda install spyder```


## 3) Install Python dependencies

This pipeline requires some dependencies which have to be installed prior to running.

They can be installed using [PIP](https://pypi.org/), by opening your terminal and running the following:

```pip3 install -r requirements.txt```

# General Settings

In order to adjust the scripts to your needs, it's necessary to create a `settings.yaml`. To do so rename the existing `example.settings.yaml` by deleting ".example".

Two settings in there are shared between all scripts:

```
testnet: true

default_output_folder: "output"
```

It's recommended to use testnet in the beginning.Testnet algos can be acquired here: https://bank.testnet.algorand.network/. If you're sure everything works as expected you can set:

`testnet: false`

The output folder for all scripts will be per default included in this folder. If you wish for your output to be generated somewhere else you can adjust that settings accordingly:

`default_output_folder: "c:/somewhere/here"`

## Video to get you started

[![Watch the video](https://imgur.com/03peyg8.png)](https://youtu.be/6luGVcjB4qk)


## Further Notice
For more information on how to setup each script look at the given examples in your `settings.yaml` or the README.md of the corresponding script. You'll only need to setup scripts you're going to use.

Finally you can check validity of your `settings.yaml` with http://www.yamllint.com/. Note also that it's necessary to use forward slashes `/` instead of backslashes in all path configurations.

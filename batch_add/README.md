# Batch adding NFTs using python

# Preparing the script

## Adjust settings.yaml

For this pipeline the following part in your `settings.yaml` must be set which will then be loaded into the main script when running.

```
# settings.yaml

batch_add:
    mnemonic1: "wreck floor carbon during taste illegal cover amused staff middle firm surface daughter pool lab update steel trophy dad twenty near kite boss abstract lens"
    input_path: "e:/algoNFTs/batch_add/example_add.csv"
```

### a) mnemonic1

This is your algorand key. Included above is a testnet account containing no real algos. In reality this should not be shared with ANYONE.

### b) input_path

This variable should point to the csv containing the assets to be added. It should contain no header and only the asset IDs to be added


# Running the script

Once you have defined your `settings.yaml`, run the script from the terminal or using your favourite IDE (open file + F5 in Spyder).

# Fetching holders of account

# Overview
This pipeline will fetch all the holders of assets created by a provided creator address. If an holder holds more than one asset by the creator, the holder address will appear multiple times in the csv.

# Download & Installation

Make sure you downloaded the whole repository and followed the steps in the main [readme](../README.md).

# Adjust settings.yaml

Using Spyder (or your favourite IDE) open "settings.yaml". All changes should be made within this file unless you need to add some additional specifications.
```
fetch_holders:
    public_key: "TIMPJ6P5FZRNNKYJLAYD44XFOSUWEOUAR6NRWJMQR66BRM3QH7UUWEHA24"
```



# Running the script

Once you have defined your parameters in the file, run the script from the terminal or using your favourite IDE (open file + F5 in Spyder).




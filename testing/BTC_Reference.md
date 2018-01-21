# How to setup a dev environement for comparing with Bitcoind?

bitcoind has a regtest mode to work on a private blockchain and test apps.  
This will allow to compare bismuth and bitcoin servers side by side, with regulat btc wallets clients for instance.

## Install bitcoind on ubuntu

```
sudo apt-get install build-essential
sudo apt-get install libtool autotools-dev autoconf
sudo apt-get install libssl-dev
sudo apt-get install libboost-all-dev
sudo add-apt-repository ppa:bitcoin/bitcoin
sudo apt-get update
sudo apt-get install bitcoind
mkdir ~/.bitcoin/
```

## Edit config

nano ~/.bitcoin/bitcoind.conf

```
rpcuser=username
rpcpassword=password
rpcport=8332
rpcallowip=127.0.0.1
server=1
```

## Start bitcoind in regtest 

`bitcoind -regtest -daemon`

## Generate some transactions

See https://bitcoin.org/en/developer-examples#regtest-mode

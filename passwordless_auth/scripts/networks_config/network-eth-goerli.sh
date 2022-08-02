#!/bin/bash
brownie networks delete goerli-alchemy
brownie networks add Ethereum goerli-alchemy host="https://eth-goerli.g.alchemy.com/v2/$WEB3_ALCHEMY_GOERLI" name='Goerli (Alchemy)' chainid=5 explorer='https://api-goerli.etherscan.io/api/'
# https://eth-goerli.g.alchemy.com/v2/

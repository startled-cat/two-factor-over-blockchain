#!/bin/bash
brownie networks delete rinkeby-alchemy
brownie networks add Ethereum rinkeby-alchemy host="https://eth-rinkeby.alchemyapi.io/v2/$WEB3_ALCHEMY_RINKEBY" name='Rinkeby (Alchemy)' chainid=4 explorer='https://api-rinkeby.etherscan.io/api/'
# https://eth-rinkeby.alchemyapi.io/v2/
brownie networks delete rinkeby
brownie networks add Ethereum rinkeby host="https://rinkeby.infura.io/v3/fa7b5430ff54496da78fe660a0be264b" name='Rinkeby (Infura)' chainid=4 explorer='https://api-rinkeby.etherscan.io/api/'

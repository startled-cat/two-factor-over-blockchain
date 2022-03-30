#!/bin/bash
brownie networks delete mumbai_moralis
brownie networks add Polygon mumbai_moralis host='https://speedy-nodes-nyc.moralis.io/f7b24c6459c3159c348cfb3e/polygon/mumbai' name='Mumbai (Moralis)' chainid=80001 explorer='https://api-testnet.polygonscan.com/api/'

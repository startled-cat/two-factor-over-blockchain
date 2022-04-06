#!/bin/bash
brownie networks delete mumbai_moralis
brownie networks add Polygon mumbai_moralis host='https://speedy-nodes-nyc.moralis.io/$WEB3_MORALIS_PROJECT_ID/polygon/mumbai' name='Mumbai (Moralis)' chainid=80001 explorer='https://api-testnet.polygonscan.com/api/'

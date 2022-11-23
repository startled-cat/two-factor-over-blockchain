#!/bin/bash
brownie networks delete kekchain
brownie networks add Kekchain kekchain host='https://testnet.kekchain.com' name='Kekchain' chainid=420666 explorer='https://testnet-explorer.kekchain.com/api/'


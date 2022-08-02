#!/bin/bash
brownie networks delete polygon-ankr
brownie networks add Polygon polygon-ankr host="https://rpc.ankr.com/polygon_mumbai" name='Polygon (ankr)' chainid=80001 explorer='https://api-testnet.polygonscan.com/api/'

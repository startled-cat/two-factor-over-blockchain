#!/bin/bash
brownie networks delete polygon-mumbai
brownie networks add Polygon polygon-mumbai host='https://polygon-mumbai.g.alchemy.com/v2/${WEB3_ALCHEMY_POLYGON}' name='Polygon Mumbai (Goërli)' chainid=80001 explorer='https://mumbai.polygonscan.com/'

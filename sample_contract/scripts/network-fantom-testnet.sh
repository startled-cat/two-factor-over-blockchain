#!/bin/bash
brownie networks delete ftm-test
brownie networks add "Fantom Opera" ftm-test host='https://rpc.testnet.fantom.network' name='Testnet' chainid=4002 explorer='https://api-testnet.ftmscan.com/api'

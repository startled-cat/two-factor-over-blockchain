#!/bin/bash
brownie networks delete avax-test
brownie networks add Avalanche avax-test host='https://api.avax-test.network/ext/bc/C/rpc' name='Testnet Fuji' chainid=43113 explorer='https://api-testnet.snowtrace.io/api'

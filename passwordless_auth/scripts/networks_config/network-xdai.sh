#!/bin/bash
brownie networks delete xdai-test-wss
brownie networks add XDai xdai-test-wss host='wss://sokol.poa.network/wss' name='Testnet wss' chainid=77 explorer='https://blockscout.com/poa/sokol/api/'
# brownie networks add Arbitrum arbitrum-testnet host='https://arb-rinkeby.g.alchemy.com/v2/${WEB3_ALCHEMY_PROJECT_ID}' name='Testnet Rinkeby' chainid=421611 explorer='http://testnet.arbiscan.io/api/'


#!/bin/bash
brownie networks delete dev-gui
brownie networks add Development dev-gui host='https://127.0.0.1:7545' name='dev gui' chainid=5777
# brownie networks add Arbitrum arbitrum-testnet host='https://arb-rinkeby.g.alchemy.com/v2/${WEB3_ALCHEMY_PROJECT_ID}' name='Testnet Rinkeby' chainid=421611 explorer='http://testnet.arbiscan.io/api/'


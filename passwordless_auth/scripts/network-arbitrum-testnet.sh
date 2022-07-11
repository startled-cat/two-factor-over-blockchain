#!/bin/bash
brownie networks delete arbitrum-testnet
brownie networks add Arbitrum arbitrum-testnet host='https://arb-rinkeby.g.alchemy.com/v2/$WEB3_ALCHEMY_PROJECT_ID' name='Testnet Rinkeby' chainid=421611 explorer='http://testnet.arbiscan.io/api/'

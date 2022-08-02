#!/bin/bash
brownie networks delete kovan-infura
brownie networks add Ethereum kovan-infura host="https://kovan.infura.io/v3/$WEB3_INFURA_KOVAN" name='Kovan (Infura2)' chainid=42 explorer='https://api-kovan.etherscan.io/api/'
# https://kovan.infura.io/v3/

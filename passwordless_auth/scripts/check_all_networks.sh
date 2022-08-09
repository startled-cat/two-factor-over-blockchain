#!/bin/bash
# network_names=(
#     xdai-test
#     aurora-test
#     harmony-testnet
#     ftm-test
#     optimism-test
#     avax-test
#     bsc-test
#     arbitrum-testnet
#     polygon-test
#     ropsten
#     goerli-alchemy
#     kovan-infura
#     rinkeby-alchemy
#     harmony-devnet
#     polygon-mumbai
#     arbitrum-testnet
# )
network_names=(
    
    arbitrum-testnet
)
for i in "${network_names[@]}"; do
    echo "checking $i ..."
    brownie run scripts/check_deployed.py --network $i
done

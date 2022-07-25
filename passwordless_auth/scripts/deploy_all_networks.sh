#!/bin/bash
network_names=(
    aurora-test
    harmony-testnet
    ftm-test
    optimism-test
    avax-test
    bsc-test
    arbitrum-testnet
    polygon-test
    ropsten
    goerli
    kovan
    rinkeby
)
for i in "${network_names[@]}"; do
    echo "Deploying to $i ..."
    brownie run scripts/deploy.py --network $i
    echo "Verifying contract at $i ..."
    brownie run scripts/verify.py --network $i
done

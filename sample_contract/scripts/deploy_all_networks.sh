#!/bin/bash
network_names=(rinkeby mumbai_moralis bsc-test arbitrum-testnet)
for i in "${network_names[@]}"; do
    echo "Deploying to $i ..."
    brownie run scripts/passwordless/deploy.py --network $i
    echo "Verifying contract at $i ..."
    brownie run scripts/passwordless/verify.py --network $i
done

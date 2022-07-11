#!/bin/bash
network_name=development
echo "Deploying to $network_name ..."
brownie run scripts/passwordless/deploy.py --network $network_name

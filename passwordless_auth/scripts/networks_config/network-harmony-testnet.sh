#!/bin/bash
brownie networks delete harmony-testnet
brownie networks add Harmony harmony-testnet host='https://api.s1.b.hmny.io' name='Harmony Testnet Shard 0' chainid=1666700000 explorer='https://explorer.pops.one/'

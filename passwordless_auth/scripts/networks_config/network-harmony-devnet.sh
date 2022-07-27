#!/bin/bash
brownie networks delete harmony-devnet
brownie networks add Harmony harmony-devnet host='https://api.s0.ps.hmny.io' name='Harmony devnet Shard 0' chainid=1666900000 explorer='https://explorer.ps.hmny.io/'

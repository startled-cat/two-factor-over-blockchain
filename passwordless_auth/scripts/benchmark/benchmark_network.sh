#!/bin/bash
brownie run scripts/benchmark/test_passwordless_performance.py --network xdai-test 2>&1 | tee ../data/benchmark/output.log
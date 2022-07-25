#!/usr/bin/zsh

project_dir="/home/adamko-wsl/git/two-factor-over-blockchain"
script_path="$project_dir/passwordless_auth/scripts/benchmark/test_passwordless_performance.py"
network_names=(
    xdai-test
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
    harmony-devnet
    polygon-mumbai
    arbitrum-testnet
)
# create directory for test results
mkdir -p "$project_dir/data/benchmark/network"
echo -n "" > "$project_dir/data/benchmark/network/networks.txt"
# for each network 
for i in "${network_names[@]}"; do
    echo "$i" >> "$project_dir/data/benchmark/network/networks.txt" 
    output_dir="$project_dir/data/benchmark/network/$i"
    mkdir -p "$output_dir"
    echo "brownie run \"$script_path\" --network $i > \"$output_dir/log_$i.log\" 2>&1"
    brownie run "$script_path" --network $i > "$output_dir/log_$i.log" 2>&1 &
done

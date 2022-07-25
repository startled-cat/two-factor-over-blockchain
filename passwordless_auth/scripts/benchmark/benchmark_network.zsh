#!/usr/bin/zsh

project_dir="/home/adamko-wsl/git/two-factor-over-blockchain"
script_path="$project_dir/passwordless_auth/scripts/benchmark/test_passwordless_performance.py"
network_names=(
    rinkeby
    kovan
    goerli
    ropsten
    polygon-mumbai
    arbitrum-testnet
    bsc-test
    avax-test
    optimism-test
    ftm-test
    harmony-devnet
    xdai-test
    aurora-test
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

#!/usr/bin/zsh
sleep_between_tests=3600
number_of_tests=72
project_dir="/home/adamko-wsl/git/two-factor-over-blockchain"
script_path="$project_dir/passwordless_auth/scripts/benchmark/test_passwordless_performance.py"
datetime=`date "+%F_%H-%M"`
network_dir="$project_dir/data/benchmark/network"

echo $network_dir
network_names=(
    ## rinkeby-alchemy
    rinkeby
    kovan-infura
    ## goerli-alchemy
    goerli
    ropsten
    ## polygon-mumbai
    polygon-ankr
    arbitrum-testnet
    bsc-test
    avax-test
    optimism-test
    ftm-test
    harmony-devnet
    xdai-test
    # xdai-test-wss
    aurora-test
)
# create directory for test results
echo "creating directory for test results ..."
mkdir -p "$network_dir"
echo -n "" > "$network_dir/networks.txt"
for i in "${network_names[@]}"; do
    echo "$i" >> "$network_dir/networks.txt"
    output_dir="$network_dir/$i"
    mkdir -p "$output_dir"
    touch "$output_dir/$i.log"
    touch "$output_dir/$i.json"
done



# run tests
echo "running tests in 10s..."
sleep 10

for i in {1..$number_of_tests}; do
    for j in "${network_names[@]}"; do
        echo "running test $i/$number_of_tests on $j ..."
        output_dir="$network_dir/$j"
        brownie run "$script_path" --network $j | tee -a "$output_dir/$j.log" &
        echo $$ >> "$output_dir/pid.txt"
    done
    echo "sleeping for $sleep_between_tests seconds ..."
    sleep $sleep_between_tests
done


# for each network 
# for i in "${network_names[@]}"; do
#     echo "$i" >> "$network_dir/networks.txt" 
#     output_dir="$network_dir/$i"
#     mkdir -p "$output_dir"
#     echo "brownie run \"$script_path\" --network $i > \"$output_dir/log_$i.log\" 2>&1"
#     brownie run "$script_path" --network $i #> "$output_dir/log_$i.log" 2>&1  &
# done

from brownie import network, accounts, config
import time
LOCAL_BLOCKCHAIN_NETWORKS = ["development", "ganache-local"]
FORKED_LOCAL_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]


def is_network_local():
    return network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_NETWORKS:
        return accounts[0]
    acc = accounts.add(config["wallets"]["from_key"])
    print(f'get_account:  {acc.address}')
    return acc


def measure_contract_stats(contract, n=3, confirmations=1, gas_limit=50_000):
    user1 = get_account(0)
    app1 = get_account(1)

    stats = []
    for _ in range(0, n):
        startTime = time.time()

        # print("giveAccess")
        userTransaction = contract.giveAccess(app1, 10, {"from": user1})
        userTransaction.wait(confirmations)

        # print("receiveAccess")
        appTransaction = contract.receiveAccess(
            user1, {"from": app1, "gas_limit": gas_limit})
        appTransaction.wait(confirmations)

        executionTime = (time.time() - startTime)
        stats.append({
            "time": executionTime,
            "userGasUsed": userTransaction.gas_used,
            "userGasPrice": userTransaction.gas_price,
            "appGasUsed": appTransaction.gas_used,
            "appGasPrice": appTransaction.gas_price,
        })
        # print(f"Execution time: {executionTime}")

        # sleepTime = random.randrange(5, 10) / 10
        # print(f"Sleeping for {sleepTime} seconds ...")
        # time.sleep(sleepTime)

    # print(f"Stats: {stats}")
    averageStats = {
        "time": sum(s["time"] for s in stats) / n,
        "userGasUsed": sum(s["userGasUsed"] for s in stats) / n,
        "userGasPrice": sum(s["userGasPrice"] for s in stats) / n,
        "appGasUsed": sum(s["appGasUsed"] for s in stats) / n,
        "appGasPrice": sum(s["appGasPrice"] for s in stats) / n,
    }

    # print(f'Execution time: {averageTime*1000}ms, {averageTime}s')
    # print(f'User cost: {averageUserGasUsed} gas')
    # print(f'App cost: {averageAppGasUsed} gas')

    return averageStats

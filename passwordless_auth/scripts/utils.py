from datetime import datetime
from brownie import network, accounts, config, chain
from brownie.network.gas.strategies import LinearScalingStrategy, ExponentialScalingStrategy
import time
LOCAL_BLOCKCHAIN_NETWORKS = ["development", "ganache-local"]
FORKED_LOCAL_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]

def get_formatted_timestamp():
    return datetime.now().strftime('%y-%m-%d %H:%M:%S')


def is_network_local():
    return network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS


def get_account(index=None, id=None):
    if index is not None:
        return accounts[index]
    if id is not None:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_NETWORKS:
        return accounts[0]
    acc = accounts.add(config["wallets"]["from_key"])
    print(f'get_account:  {acc.address}')
    return acc


def measure_contract_stats(contract, n=3, confirmations=1):
    if is_network_local():
        user1 = get_account(0)
        app1 = get_account(1)
    else:
        user1 = get_account(index=2)
        app1 = get_account(index=1)

    print(f'user1: {user1.address}')
    print(f'app1: {app1.address}')

    # network.gas_price("auto")

    # gas_strategy = ExponentialScalingStrategy(
    #     "100000 wei", "100 gwei", time_duration=10)

    # gas_strategy = LinearScalingStrategy(
    #     "100000 wei", "100 gwei", increment=1.1, time_duration=3)
    # network.gas_price(gas_strategy)

    stats = []
    for _ in range(0, n):

        x = {
            "network": network.show_active(),
            "confirmations": confirmations,

            "timestamp": time.time(),
            
            "fee": network.priority_fee(),

            "user_hash":None,
            "user_timestamp":None,
            "user_time": None,
            "user_tx_status": None,
            "user_gas_used": None,
            "user_gas_price": None,
            "user_cost": None,
            "user_error": None,

            "app_hash":None,
            "app_timestamp":None,
            "app_time": None,
            "app_tx_status": None,
            "app_gas_used": None,
            "app_gas_price": None,
            "app_cost": None,
            "app_error": None,
        }
        
        def fill(confirmation_times, tx, prefix):
            x[prefix+"_hash"] = tx.txid
            x[prefix+"_timestamp"] = tx.timestamp
            x[prefix+"_time"] = confirmation_times
            x[prefix+"_tx_status"] = tx.status
            x[prefix+"_gas_used"] = tx.gas_used
            x[prefix+"_gas_price"] = tx.gas_price
            x[prefix+"_cost"] = tx.gas_used * tx.gas_price

        try:
            confirmation_times, tx = execute_contract_function(
                contract, "giveAccess", {"from": user1, "gas_limit": 75_000}, args=[app1, 3200], confirmations=confirmations, retires=5)
            fill(confirmation_times, tx, "user")
        except Exception as e:
            x["user_tx_status"] = -2
            x["user_error"] = str(e)
            print(e)
        finally:
            pass

        try:
            confirmation_times, tx = execute_contract_function(
                contract, "receiveAccess", {"from": app1, "gas_limit": 35_000}, args=[user1], confirmations=confirmations, retires=5)
            fill(confirmation_times, tx, "app")
        except Exception as e:
            x["app_tx_status"] = -2
            x["app_error"] = str(e)
            print(e)
        finally:
            pass

        stats.append(x)

    return stats


def execute_contract_function(contract, function_name, tx_params, args=[], confirmations=1, retires=0):

    try:
        confirmation_times = []
        start_time = time.time()
        tx = getattr(contract, function_name)(*args, tx_params)

        for c in range(1, confirmations+1):
            print(f"{get_formatted_timestamp()} > waiting for {c} confirmations...")
            tx.wait(c)
            confirmation_times.append(time.time() - start_time)
            print("last confirmations time: ", confirmation_times[-1])

        return confirmation_times, tx
    except Exception as e:
        print(f"{get_formatted_timestamp()} > Transaction failed:", e)
        if retires > 0:
            print(f"{get_formatted_timestamp()} > Retrying in 10s...(retries left:", retires, ")")
            time.sleep(10)
            return execute_contract_function(contract, function_name, tx_params, args, confirmations, retires-1)
        else:
            raise e

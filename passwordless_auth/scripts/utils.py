import random
import threading
from brownie import Wei
from datetime import datetime
from brownie import network, accounts, config, chain, web3
from brownie.network.gas.strategies import LinearScalingStrategy, ExponentialScalingStrategy
import time
LOCAL_BLOCKCHAIN_NETWORKS = ["development", "ganache-local"]
FORKED_LOCAL_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]


# convert any variable to int, if error, then return 0
def to_int(value):
    try:
        return int(value)
    except:
        return 0

def get_formatted_timestamp():
    return datetime.now().strftime('%y-%m-%d %H:%M:%S')


def log_prefix(error=False):
    m = "ERROR" if error else "INFO"
    return f'[{network.show_active()}][{m}][{get_formatted_timestamp()}] '


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

class WaitForConfirmationsThread(threading.Thread):
    def __init__(self, tx, confirmations):
        threading.Thread.__init__(self)
        self.tx = tx
        self.confirmations = confirmations

    def run(self):
        try:
            self.tx.wait(self.confirmations)
        except Exception as e:
            print(f"{log_prefix(error=True)} in waiting thread:  {e}")
            
def measure_contract_stats(contract, n=1, confirmations=5):
    if is_network_local():
        user1 = get_account(0)
        app1 = get_account(1)
    else:
        available_accounts_indexes = [-2, -1]
        # randomize the accounts order
        random.shuffle(available_accounts_indexes)
        user1 = get_account(index=available_accounts_indexes[0])
        app1 = get_account(index=available_accounts_indexes[1])

    user_balance = to_int(user1.balance())
    print(f'{log_prefix()}user1: {user1.address}')
    print(f'{log_prefix()}{Wei(user_balance).to("ether")} eth; {Wei(user_balance).to("gwei")} gwei; {(user_balance)} wei')
    app_balance = to_int(app1.balance())
    print(f'{log_prefix()}app1: {app1.address}')
    print(f'{log_prefix()}{Wei(app_balance).to("ether")} eth; {Wei(app_balance).to("gwei")} gwei; {(app_balance)} wei')


    # network.gas_price("auto")

    # gas_strategy = ExponentialScalingStrategy(
    #     "100000 wei", "100 gwei", time_duration=10)

    # gas_strategy = LinearScalingStrategy(
    #     "100000 wei", "100 gwei", increment=1.1, time_duration=3)
    # network.gas_price(gas_strategy)

    stats = []
    for _ in range(0, n):
        print(f"{log_prefix()} measuring contract stats..., test {_+1}/{n}")
        x = {
            "network": network.show_active(),
            "confirmations": confirmations,

            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),

            "fee": network.priority_fee(),

            "user_hash": None,
            "user_timestamp": None,
            "user_time": None,
            "user_tx_status": None,
            "user_gas_used": None,
            "user_gas_price": None,
            "user_cost": None,
            "user_error": None,

            "app_hash": None,
            "app_timestamp": None,
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
            x[prefix+"_gas_used"] = to_int(tx.gas_used)
            x[prefix+"_gas_price"] = to_int(tx.gas_price)
            x[prefix+"_cost"] = to_int(tx.gas_used) * to_int(tx.gas_price)

        try:
            confirmation_times, tx = execute_contract_function(
                contract, "giveAccess",
                {"from": user1, "gas_limit": 1_000_000, "required_confs": 0},
                args=[app1, 3200],
                confirmations=confirmations,
                retires=8)
            fill(confirmation_times, tx, "user")
        except Exception as e:
            x["user_tx_status"] = -2
            x["user_error"] = str(e)
            print(f"{log_prefix(error=True)}" ,e)
        finally:
            pass
        
        
        waited_for = 0
        check_access_result = None
        while True:
            check_access_result = contract.checkAccess(user1, app1, {"from": app1})
            print(f"{log_prefix()} check_access_result: {check_access_result}")
            if check_access_result:
                break
            else:
                time.sleep(1)
                waited_for += 1
                if waited_for > 60:
                    check_access_result = False
                    break
                    
        if check_access_result == False:
            print(f"{log_prefix(error=True)} checkAccess failed after {waited_for} seconds")
            continue

        
        try:
            confirmation_times, tx = execute_contract_function(
                contract, "receiveAccess",
                {"from": app1, "gas_limit": 1_000_000, "required_confs": 0},
                args=[user1],
                confirmations=confirmations,
                retires=10)
            fill(confirmation_times, tx, "app")
        except Exception as e:
            x["app_tx_status"] = -2
            x["app_error"] = str(e)
            print(f"{log_prefix(error=True)}" ,e)
        finally:
            pass

        stats.append(x)
        try:
            print(f"{log_prefix()} user balance enough for : {user_balance / x['user_cost']} transactions")
            print(f"{log_prefix()} app balance enough for  : {app_balance / x['app_cost']} transactions")
        except Exception as e:
            print(f"{log_prefix(error=True)}", e)

    return stats


def execute_contract_function(contract, function_name, tx_params, args=[], confirmations=1, retires=0, retry_sleep=10):

    try:
        confirmation_times = []
        start_time = time.time()
        print(f"{log_prefix()} executing '{function_name}' with args: {args}")
        tx = getattr(contract, function_name)(*args, tx_params)

        for c in range(1, confirmations+1):
            print(f"{log_prefix()} waiting for {c} confirmations...")

            # """can break and never end"""
            # tx.wait(c)
            
            # """ makes too much rpc calls """
            # waited_for = 0
            # while tx.confirmations < c:
            #     time.sleep(0.1)
            #     waited_for += 0.1
            #     if waited_for > 300:
            #         print(
            #             f"{log_prefix()} timed out while waiting for {c} confirmations")
            #         break
            
            confirmations_thread = WaitForConfirmationsThread(tx, c)
            confirmations_thread.start()
            confirmations_thread.join(timeout=300)
            if confirmations_thread.is_alive():
                print(f"{log_prefix(error=True)} confirmations_thread timed out while waiting for {c} confirmations")
                confirmation_times.append(0)
                continue
                
            confirmation_times.append(time.time() - start_time)
            print(f"{log_prefix()} last confirmations time: ",
                  confirmation_times[-1])

        return confirmation_times, tx
    except Exception as e:
        print(f"{log_prefix(error=True)} Transaction failed:", e)
        if retires > 0:
            print(
                f"{log_prefix()} Retrying in {retry_sleep} s...(retries left:", retires, ")")
            time.sleep(retry_sleep)
            tx_params["nonce"] = web3.eth.get_transaction_count(tx_params["from"].address)+1
            return execute_contract_function(contract, function_name, tx_params, args, confirmations, retires-1, retry_sleep=retry_sleep*1.5)
        else:
            raise e



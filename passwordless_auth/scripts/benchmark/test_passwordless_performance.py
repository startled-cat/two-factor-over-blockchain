from scripts.utils import get_account, get_formatted_timestamp, measure_contract_stats, is_network_local
from brownie import PasswordlessAuthentication, network, accounts, config, chain
from scripts.deploy import deploy
import threading
from brownie import chain
import time
import json
from tinydb import TinyDB, Query
from datetime import datetime

class LocalChainMineThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        time.sleep(0.5)
        self.running = True
        while self.running:
            try:
                chain.mine()
                print("LocalChainMineThread: chain.mine()")
                time.sleep(1)
            except:
                time.sleep(3)

    def stop(self):
        self.running = False


def execute_single_test(contract, db_path):
    try:
        stats = measure_contract_stats(
            contract, n=1, confirmations=5)
        with TinyDB(db_path) as db:
            for s in stats:
                db.insert(s)
    except Exception as e:
        print(e)


def test_speed():
    
    runs_per_h = 3
    total_test_time = 12
    
    total_runs = runs_per_h * total_test_time
    sleep_between_runs = 3600 / runs_per_h
    
    # total_runs = 1
    # sleep_between_runs = 0
    
    if len(PasswordlessAuthentication) < 1:
        deploy()
    contract = PasswordlessAuthentication[-1]

    if is_network_local():
        thread = LocalChainMineThread()
        thread.start()
    else:
        accounts.add(config["wallets"]["from_key"])
        accounts.add(config["wallets"]["from_key2"])

    db_path = f'../data/benchmark/{network.show_active()}_{total_runs}_{datetime.now().strftime("%y%m%d-%H%M")}.json'
    with TinyDB(db_path) as db:
        db.drop_tables()
        db.close()

    test_thread = None
    for _ in range(0, total_runs):
        print("============================================================================")
        print("============================================================================")
        print(f"        Current datetime : {get_formatted_timestamp()}")
        print(f"        Running test no: {_+1}/{total_runs}; tests per hour: {runs_per_h}, total test time: {total_test_time}")
        print("============================================================================")
        print("============================================================================")
        
        test_thread = threading.Thread(target=execute_single_test,
                                       args=(contract, db_path))
        test_thread.start()
        time.sleep(sleep_between_runs)

    if is_network_local():
        test_thread.join()
        time.sleep(10)
        thread.stop()
        thread.join()


def main():
    test_speed()


if __name__ == "__main__":
    main()

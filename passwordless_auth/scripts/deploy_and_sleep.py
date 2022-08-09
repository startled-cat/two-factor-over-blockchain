
from brownie import PasswordlessAuthentication, network, Wei, chain
from scripts.utils import get_account

import time

def deploy():
    app_account = get_account(0)
    user_account = get_account(1)
    
    # print addresses and private keys of accounts
    print(f"app_account: {app_account.address}")
    print(f"user_account: {user_account.address}")
    
    
    contract = PasswordlessAuthentication.deploy(
        {"from": app_account, "allow_revert": False, "gas_limit": 10_000_000})
    print(
        f"PasswordlessAuthentication has been deployed at {network.show_active()} address: {contract.address}")
    return contract


def main():
    deploy()
    print("Deployed")
    while True:
        time.sleep(1)
        chain.mine()
        print("Mined")
        
# compare lgbt levels of a borys and a bald




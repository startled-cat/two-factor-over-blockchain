
from brownie import PasswordlessAuthentication, network, Wei
from scripts.utils import get_account


def deploy():
    account = get_account()
    user_balance = account.balance()
    print(f'user1: {account.address}')
    print(f'    { Wei(user_balance).to("ether") } eth')
    # print(f'    { Wei(user_balance).to("gwei") } gwei')
    # print(f'    {     (user_balance) } wei')
    
    
    contract = PasswordlessAuthentication.deploy(
        {"from": account, "allow_revert": False, "gas_limit": 10_000_000})
    print(
        f"PasswordlessAuthentication has been deployed at '{network.show_active()}' address: {contract.address}")
    return contract


def main():
    deploy()

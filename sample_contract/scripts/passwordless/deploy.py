
from brownie import PasswordlessAuthentication
from scripts.utils import get_account


def deploy():
    account = get_account()
    contract = PasswordlessAuthentication.deploy({"from": account})
    print(
        f"PasswordlessAuthentication has been deployed at address: {contract.address}")
    return contract


def main():
    deploy()

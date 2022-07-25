
from brownie import PasswordlessAuthentication, network
from scripts.utils import get_account


def check_deployed():
    contract = PasswordlessAuthentication[-1]
    print(f"network: {network.show_active()}, contract at: {contract.address}")


def main():
    check_deployed()

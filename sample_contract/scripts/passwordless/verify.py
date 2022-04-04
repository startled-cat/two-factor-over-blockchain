
from brownie import PasswordlessAuthentication


def verify():
    contract = PasswordlessAuthentication[-1]
    print(f"Verifying contract at: {contract.address} ...")
    PasswordlessAuthentication.publish_source(contract)
    return contract


def main():
    verify()

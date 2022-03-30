
from brownie import AuthenticatorProvider
from scripts.utils import get_account


def deploy():
    account = get_account()
    authenticatorProvider = AuthenticatorProvider.deploy({"from": account})
    print(
        f"AuthenticatorProvider has been deployed at address: {authenticatorProvider.address}")
    return authenticatorProvider


def main():
    deploy()

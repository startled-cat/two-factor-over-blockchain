
from brownie import AuthenticatorProvider


def verify():
    authenticatorProvider = AuthenticatorProvider[-1]
    print(f"Verifying contract at: {authenticatorProvider.address} ...")
    AuthenticatorProvider.publish_source(authenticatorProvider)
    return authenticatorProvider


def main():
    verify()

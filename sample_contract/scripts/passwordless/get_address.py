from brownie import PasswordlessAuthentication, network


def check():
    contract = PasswordlessAuthentication[-1]
    print(f"Using network: {network.show_active()}")
    print(
        f"Last deployed PasswordlessAuthentication at : {contract.address}")


def main():
    check()

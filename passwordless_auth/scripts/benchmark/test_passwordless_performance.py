from scripts.utils import get_account, measure_contract_stats
from brownie import PasswordlessAuthentication
from scripts.deploy import deploy


def test_speed():
    if len(PasswordlessAuthentication) < 1:
        deploy()
    contract = PasswordlessAuthentication[-1]
    stats = measure_contract_stats(contract)
    print(stats)


def main():
    test_speed()


if __name__ == "__main__":
    main()

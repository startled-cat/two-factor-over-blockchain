from brownie import network, config, PasswordlessAuthentication
from scripts.utils import get_account, is_network_local
from scripts.passwordless.deploy import deploy
import pytest


def test_passwordlessDeployment():
    if not is_network_local():
        pytest.skip("Only for unit testing")
    contract = deploy()


def test_checkAccess():
    if not is_network_local():
        pytest.skip("Only for unit testing")

    contract = deploy()
    account1 = get_account(0)
    account2 = get_account(1)
    assert False == contract.checkAccess(account1, account2)


def test_givenAccessUntill():
    if not is_network_local():
        pytest.skip("Only for unit testing")
    contract = deploy()
    account1 = get_account(0)
    account2 = get_account(1)
    assert contract.givenAccessUntill(account2, account2) == 0
    assert contract.givenAccessUntill(account1, account2) == 0
    assert contract.givenAccessUntill(account2, account1) == 0
    assert contract.givenAccessUntill(account1, account1) == 0


def test_giveAccess():
    if not is_network_local():
        pytest.skip("Only for unit testing")

    contract = deploy()
    account1 = get_account(0)
    account2 = get_account(1)
    contract.giveAccess(account2, 0, {"from": account1})
    assert True == contract.checkAccess(account1, account2)
    contract.giveAccess(account2, 100, {"from": account1})
    assert True == contract.checkAccess(account1, account2)
    assert False == contract.checkAccess(account2, account1)


def test_receiveAccess():
    if not is_network_local():
        pytest.skip("Only for unit testing")

    contract = deploy()
    account1 = get_account(0)
    account2 = get_account(1)

    assert False == contract.checkAccess(account1, account2)
    contract.giveAccess(account2, 100, {"from": account1})
    assert True == contract.checkAccess(account1, account2)
    tx = contract.receiveAccess(account1, {"from": account2})
    tx.wait(1)
    print(tx)

    # assert False == contract.checkAccess(account1, account2)
    # assert False == contract.receiveAccess(account1, {"from": account2})

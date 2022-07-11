from brownie import network, config, PasswordlessAuthentication, chain, exceptions
from scripts.utils import get_account, is_network_local
from scripts.passwordless.deploy import deploy
from utils import only_local
import pytest
import time


@only_local
def test_passwordlessDeployment():
    contract = deploy()
    print(contract)


@only_local
def test_give_and_check_access():
    contract = deploy()
    user1 = get_account(0)
    user2 = get_account(1)
    app1 = get_account(2)
    app2 = get_account(3)

    with pytest.raises(OverflowError):
        contract.giveAccess(app1, -1, {"from": user1})
    with pytest.raises(exceptions.VirtualMachineError):
        contract.giveAccess(app1, 3601, {"from": user1})
    with pytest.raises(exceptions.VirtualMachineError):
        contract.giveAccess(app1, 0, {"from": user1})
    with pytest.raises(exceptions.VirtualMachineError):
        contract.giveAccess(app1, "10", {"from": app1})

    assert False == contract.checkAccess(user1, app1)
    assert False == contract.checkAccess(user2, app2)
    assert False == contract.checkAccess(user1, app2)
    assert False == contract.checkAccess(user2, app1)
    contract.giveAccess(app1, 1, {"from": user1})
    assert True == contract.checkAccess(user1, app1)
    assert False == contract.checkAccess(user2, app2)
    assert False == contract.checkAccess(user1, app2)
    assert False == contract.checkAccess(user2, app1)
    contract.giveAccess(app2, 10, {"from": user2})
    assert True == contract.checkAccess(user1, app1)
    assert True == contract.checkAccess(user2, app2)
    assert False == contract.checkAccess(user1, app2)
    assert False == contract.checkAccess(user2, app1)
    time.sleep(2)
    chain.mine(1)
    assert False == contract.checkAccess(user1, app1)
    assert True == contract.checkAccess(user2, app2)
    assert False == contract.checkAccess(user1, app2)
    assert False == contract.checkAccess(user2, app1)


@only_local
def test_receiveAccess():

    contract = deploy()
    user1 = get_account(0)
    user2 = get_account(1)
    app1 = get_account(2)
    app2 = get_account(3)

    with pytest.raises(exceptions.VirtualMachineError):
        contract.receiveAccess(app1, {"from": user1, "gas_limit": 50_000})

    contract.giveAccess(app1, 1, {"from": user1, "gas_limit": 50_000})
    assert True == contract.checkAccess(user1, app1)
    tx = contract.receiveAccess(user1, {"from": app1, "gas_limit": 50_000})
    tx.wait(1)
    assert False == contract.checkAccess(user1, app1)

    with pytest.raises(exceptions.VirtualMachineError):
        contract.receiveAccess(app1, {"from": user1, "gas_limit": 50_000})

    contract.giveAccess(app1, 1, {"from": user1, "gas_limit": 50_000})
    assert True == contract.checkAccess(user1, app1)
    time.sleep(2)
    chain.mine(1)
    with pytest.raises(exceptions.VirtualMachineError):
        contract.receiveAccess(user1, {"from": app1, "gas_limit": 50_000})

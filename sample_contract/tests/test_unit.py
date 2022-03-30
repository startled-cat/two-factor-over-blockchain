from brownie import network, config, AuthenticatorProvider
from scripts.utils import get_account, is_network_local
from scripts.deploy import deploy

import pytest


def test_deployment():
    if not is_network_local():
        pytest.skip("Only for unit testing")
    contract = deploy()


def test_getNewOtp():
    if not is_network_local():
        pytest.skip("Only for unit testing")

    contract = contract = deploy()

    otp1 = contract.getNewOtp()
    otp2 = contract.getNewOtp()
    if otp1 != otp2:
        pytest.warnings.warn(UserWarning("Otp is not truly random"))

    otp1 = contract.getNewOtp({"from": get_account(0)})
    otp2 = contract.getNewOtp({"from": get_account(1)})
    assert otp1 != otp2

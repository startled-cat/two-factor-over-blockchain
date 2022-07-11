from brownie import network, config, AuthenticatorProvider
from scripts.utils import get_account, is_network_local
from scripts.deploy import deploy

import pytest


def test_generate_otp():
    pytest.skip("skipping otp contract test")
    if is_network_local():
        pytest.skip("Only for integration testing")
    contract = AuthenticatorProvider[-1]
    account = get_account(0)
    tx = contract.generateOtp(account.address, {"from": account})
    (password, generatedAt) = contract.otp(account.address)
    assert len(str(password)) > 0

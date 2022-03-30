from brownie import network, config, AuthenticatorProvider
from scripts.utils import get_account, is_network_local
from scripts.deploy import deploy

import pytest


def test_deployment():
    if not is_network_local():
        pytest.skip("Only for integration testing")
    contract = deploy()

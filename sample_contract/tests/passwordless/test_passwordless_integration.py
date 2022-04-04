from brownie import network, config, PasswordlessAuthentication
from scripts.utils import get_account, is_network_local
from scripts.passwordless.deploy import deploy
import pytest

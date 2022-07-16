from scripts.utils import is_network_local
from scripts.deploy import deploy

import pytest


def only_local(func):
    def decorator(*args, **kwargs):
        if not is_network_local():
            pytest.skip("Only for unit testing")
        func(*args, **kwargs)
    return decorator


def deploy_contract(func):
    def decorator(*args, **kwargs):
        kwargs["contract"] = deploy()
        func(*args, **kwargs)
    return decorator

from scripts.utils import is_network_local
import pytest


def only_local(func):
    def decorator(*args, **kwargs):
        if not is_network_local():
            pytest.skip("Only for unit testing")
        func(*args, **kwargs)
    return decorator

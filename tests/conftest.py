import logging

import pytest


@pytest.fixture
def log(caplog):
    caplog.set_level(logging.DEBUG)
    return caplog

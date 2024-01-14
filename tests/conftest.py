from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi.log import logger
from tests import AwaitLog


@pytest.fixture()
def await_log() -> Generator[AwaitLog, None, None]:
    handler = AwaitLog()
    logger.addHandler(handler)
    try:
        yield handler
    finally:
        logger.removeHandler(handler)

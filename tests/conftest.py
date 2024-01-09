from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi.radio import Radio
from tests import QueueRunner, running


@pytest.fixture()
def runner() -> QueueRunner:
    return QueueRunner()


@pytest.fixture()
def radio(runner: QueueRunner) -> Generator[Radio, None, None]:
    with running(runner=runner) as radio:
        yield radio

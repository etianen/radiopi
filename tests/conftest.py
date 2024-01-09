from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi.radio import Radio
from tests import TestRunner, running


@pytest.fixture()
def runner() -> TestRunner:
    return TestRunner()


@pytest.fixture()
def radio(runner: TestRunner) -> Generator[Radio, None, None]:
    with running(runner=runner) as radio:
        yield radio

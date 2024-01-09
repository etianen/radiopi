from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi import running
from radiopi.radio import Radio
from radiopi.runner import create_runner


@pytest.fixture()
def radio() -> Generator[Radio, None, None]:
    with running(pin_factory_name="mock", runner=create_runner("mock")) as machine:
        yield machine

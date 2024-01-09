from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi import running
from radiopi.radio import Radio
from radiopi.runner import mock_runner


@pytest.fixture()
def radio() -> Generator[Radio, None, None]:
    with running(pin_factory_name="mock", runner=mock_runner) as machine:
        yield machine

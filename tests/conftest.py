from __future__ import annotations

from collections.abc import Generator, Sequence

import pytest

from radiopi import running
from radiopi.radio import Radio


@pytest.fixture()
def radio() -> Generator[Radio, None, None]:
    with running(pin_factory_name="mock") as machine:
        yield machine

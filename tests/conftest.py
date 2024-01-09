from __future__ import annotations

import pytest

from radiopi.radio import Radio


@pytest.fixture()
def radio() -> Radio:
    return Radio()

from __future__ import annotations

from collections.abc import Generator, Sequence

import pytest

from radiopi import running
from radiopi.pins import MOCK_PIN_FACTORY_NAME
from radiopi.radio import Radio


@pytest.fixture()
def radio() -> Generator[Radio, None, None]:
    with running(pin_factory_name=MOCK_PIN_FACTORY_NAME) as machine:
        yield machine


# @pytest.fixture()
# def radio(stations: Sequence[Station]) -> Generator[Radio, None, None]:
#     # Create radio.
#     radio = Radio(
#         pin_factory=MockFactory(),
#         run=run_mock,
#         stations=stations,
#     )
#     # Run radio.
#     with radio.running():
#         yield radio

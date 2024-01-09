from __future__ import annotations

from collections.abc import Generator, Sequence

import pytest

from radiopi.pins import PinFactory, create_pin_factory
from radiopi.stations import Station, load_stations


@pytest.fixture(scope="session")
def stations() -> Sequence[Station]:
    return load_stations()


@pytest.fixture()
def pin_factory() -> Generator[PinFactory, None, None]:
    with create_pin_factory("mock") as pin_factory:
        yield pin_factory


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

from __future__ import annotations

import logging
from collections.abc import Generator, Sequence

import pytest
from gpiozero.pins.mock import MockFactory

from radiopi.radio import Radio
from radiopi.run import run_mock
from radiopi.stations import Station, load_stations


@pytest.fixture(scope="session", autouse=True)
def logging_config() -> None:
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)


@pytest.fixture(scope="session")
def stations() -> Sequence[Station]:
    return load_stations()


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

from __future__ import annotations

import logging
from collections.abc import Generator

import pytest
from gpiozero.pins.mock import MockFactory

from radiopi.radio import Radio
from radiopi.run import run_mock


@pytest.fixture(scope="session", autouse=True)
def logging_config() -> None:
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)


@pytest.fixture()
def radio() -> Generator[Radio, None, None]:
    # Create radio.
    radio = Radio(
        pin_factory=MockFactory(),
        run=run_mock,
        stations=(),
    )
    # Run radio.
    with radio.running():
        yield radio

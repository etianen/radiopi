from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi.log import logger
from radiopi.radio import Radio, radio_boot_args, radio_tune_args
from tests import AwaitLog, LogMessage, running


@pytest.fixture()
def await_log() -> Generator[AwaitLog, None, None]:
    handler = AwaitLog()
    logger.addHandler(handler)
    try:
        yield handler
    finally:
        logger.removeHandler(handler)


@pytest.fixture()
def radio(await_log: AwaitLog) -> Generator[Radio, None, None]:
    with running() as radio:
        # Wait for the radio to boot and tune.
        await_log(LogMessage.runner_call(radio_boot_args()))
        await_log(LogMessage.runner_call(radio_tune_args(radio.state.stations[0])))
        # All done!
        yield radio

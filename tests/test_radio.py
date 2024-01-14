from __future__ import annotations

import pytest

from tests import AwaitLog, ExpectedLog, running


def test_running_pause_on_stop(await_log: AwaitLog) -> None:
    with running() as radio:
        # On start, the radio will boot and tune.
        await_log(ExpectedLog.radio_boot())
        await_log(ExpectedLog.radio_tune(radio.state.stations[0]))
    # On stop, the radio automatically pauses.
    await_log(ExpectedLog.radio_pause())


def test_running_pause_on_stop_already_paused(await_log: AwaitLog) -> None:
    with running() as radio:
        # On start, the radio will boot and tune.
        await_log(ExpectedLog.radio_boot())
        await_log(ExpectedLog.radio_tune(radio.state.stations[0]))
        # Pause the radio.
        radio.pause()
        await_log(ExpectedLog.radio_pause())
    # On stop, since the radio is already paused, nothing needs to be done.
    with pytest.raises(AssertionError):
        await_log(ExpectedLog.radio_pause())

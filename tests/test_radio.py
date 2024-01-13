from __future__ import annotations

import pytest

from radiopi.radio import Radio
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


def test_pause(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.radio_pause())


def test_toggle_play(radio: Radio, await_log: AwaitLog) -> None:
    # This will pause the radio.
    radio.toggle_play()
    await_log(ExpectedLog.radio_pause())
    # This will start the radio playing.
    radio.toggle_play()
    await_log(ExpectedLog.radio_boot())
    await_log(ExpectedLog.radio_tune(radio.state.stations[0]))


def test_pause_pause_play(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.radio_pause())
    # This second pause does nothing, since we're already paused.
    radio.pause()
    # This play results in an action.
    radio.play()
    await_log(ExpectedLog.radio_boot())
    await_log(ExpectedLog.radio_tune(radio.state.stations[0]))


def test_play_play_pause(radio: Radio, await_log: AwaitLog) -> None:
    # These plays do nothing, since we're already playing.
    radio.play()
    radio.play()
    # This pause results in an action.
    radio.pause()
    await_log(ExpectedLog.radio_pause())


def test_next_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.next_station()
    # We're already booted, so we just tune.
    await_log(ExpectedLog.radio_tune(radio.state.stations[1]))


def test_prev_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.prev_station()
    # We're already booted, so we just tune.
    await_log(ExpectedLog.radio_tune(radio.state.stations[-1]))


def test_pause_next_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.radio_pause())
    # Since we're paused, this will first boot, then tune.
    radio.next_station()
    await_log(ExpectedLog.radio_boot())
    await_log(ExpectedLog.radio_tune(radio.state.stations[1]))

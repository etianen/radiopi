from __future__ import annotations

from collections.abc import Generator

import pytest

from radiopi.radio import Radio
from tests import AwaitLog, ExpectedLog, running


@pytest.fixture()
def radio(await_log: AwaitLog) -> Generator[Radio, None, None]:
    with running() as radio:
        # Wait for the radio to boot and tune.
        await_log(ExpectedLog.ux_tune(radio.state.stations[0]))
        # All done!
        yield radio


def test_pause(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.ux_pause())


def test_toggle_play(radio: Radio, await_log: AwaitLog) -> None:
    # This will pause the radio.
    radio.toggle_play()
    await_log(ExpectedLog.ux_pause())
    # This will start the radio playing.
    radio.toggle_play()
    await_log(ExpectedLog.ux_tune(radio.state.stations[0]))


def test_pause_pause_play(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.ux_pause())
    # This second pause does nothing, since we're already paused.
    radio.pause()
    # This play results in an action.
    radio.play()
    await_log(ExpectedLog.ux_tune(radio.state.stations[0]))


def test_play_play_pause(radio: Radio, await_log: AwaitLog) -> None:
    # These plays do nothing, since we're already playing.
    radio.play()
    radio.play()
    # This pause results in an action.
    radio.pause()
    await_log(ExpectedLog.ux_pause())


def test_next_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.next_station()
    # We're already booted, so we just tune.
    await_log(ExpectedLog.ux_next_station(radio.state.stations[1]))


def test_prev_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.prev_station()
    # We're already booted, so we just tune.
    await_log(ExpectedLog.ux_prev_station(radio.state.stations[-1]))


def test_pause_next_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.ux_pause())
    # Since we're paused, this will first boot, then tune.
    radio.next_station()
    await_log(ExpectedLog.ux_tune(radio.state.stations[1]))


def test_pause_prev_station(radio: Radio, await_log: AwaitLog) -> None:
    radio.pause()
    await_log(ExpectedLog.ux_pause())
    # Since we're paused, this will first boot, then tune.
    radio.prev_station()
    await_log(ExpectedLog.ux_tune(radio.state.stations[-1]))

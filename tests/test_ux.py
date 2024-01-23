from __future__ import annotations

from collections.abc import Generator

import pytest
from logot import Logot

from radiopi.radio import Radio
from tests import logged, running


@pytest.fixture()
def radio(logot: Logot) -> Generator[Radio, None, None]:
    with running() as radio:
        # Wait for the radio to boot and tune.
        logot.wait_for(logged.ux_tune(radio.state.stations[0]))
        # All done!
        yield radio


def test_pause(radio: Radio, logot: Logot) -> None:
    radio.pause()
    logot.wait_for(logged.ux_pause())


def test_toggle_play(radio: Radio, logot: Logot) -> None:
    # This will pause the radio.
    radio.toggle_play()
    logot.wait_for(logged.ux_pause())
    # This will start the radio playing.
    radio.toggle_play()
    logot.wait_for(logged.ux_tune(radio.state.stations[0]))


def test_pause_pause_play(radio: Radio, logot: Logot) -> None:
    radio.pause()
    logot.wait_for(logged.ux_pause())
    # This second pause does nothing, since we're already paused.
    radio.pause()
    # This play results in an action.
    radio.play()
    logot.wait_for(logged.ux_tune(radio.state.stations[0]))


def test_play_play_pause(radio: Radio, logot: Logot) -> None:
    # These plays do nothing, since we're already playing.
    radio.play()
    radio.play()
    # This pause results in an action.
    radio.pause()
    logot.wait_for(logged.ux_pause())


def test_retune(radio: Radio, logot: Logot) -> None:
    radio.retune(3)
    # We're already booted, so we just tune.
    logot.wait_for(logged.ux_retune(radio.state.stations[3]))


def test_next_station(radio: Radio, logot: Logot) -> None:
    radio.next_station()
    # We're already booted, so we just tune.
    logot.wait_for(logged.ux_next_station(radio.state.stations[1]))


def test_prev_station(radio: Radio, logot: Logot) -> None:
    radio.prev_station()
    # We're already booted, so we just tune.
    logot.wait_for(logged.ux_prev_station(radio.state.stations[-1]))


def test_pause_next_station(radio: Radio, logot: Logot) -> None:
    radio.pause()
    logot.wait_for(logged.ux_pause())
    # Since we're paused, this will first boot, then tune.
    radio.next_station()
    logot.wait_for(logged.ux_tune(radio.state.stations[1]))


def test_pause_prev_station(radio: Radio, logot: Logot) -> None:
    radio.pause()
    logot.wait_for(logged.ux_pause())
    # Since we're paused, this will first boot, then tune.
    radio.prev_station()
    logot.wait_for(logged.ux_tune(radio.state.stations[-1]))

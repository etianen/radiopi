from __future__ import annotations

from queue import Empty

import pytest

from radiopi.radio import Radio, radio_boot_args, radio_pause_args, radio_tune_args
from tests import TestRunner, running


def test_running_pause_on_stop(runner: TestRunner) -> None:
    with running(runner=runner):
        pass
    # On stop, the radio automatically pauses.
    runner.assert_called(radio_pause_args())


def test_running_pause_on_stop_already_paused(runner: TestRunner) -> None:
    with running(runner=runner) as radio:
        # Pause the radio.
        radio.pause()
        runner.assert_called(radio_pause_args())
    # On stop, since the radio is already paused, nothing needs to be done.
    with pytest.raises(Empty):
        runner.queue.get_nowait()


def test_pause(radio: Radio, runner: TestRunner) -> None:
    radio.pause()
    runner.assert_called(radio_pause_args())


def test_pause_pause_play(radio: Radio, runner: TestRunner) -> None:
    radio.pause()
    runner.assert_called(radio_pause_args())
    # This second pause does nothing, since we're already paused.
    radio.pause()
    # This play results in an action.
    radio.play()
    runner.assert_called(radio_boot_args())
    runner.assert_called(radio_tune_args(radio.state.stations[0]))


def test_play_play_pause(radio: Radio, runner: TestRunner) -> None:
    # These plays do nothing, since we're already playing.
    radio.play()
    radio.play()
    # This pause results in an action.
    radio.pause()
    runner.assert_called(radio_pause_args())


def test_next_station(radio: Radio, runner: TestRunner) -> None:
    radio.next_station()
    # We're already booted, so we just tune.
    runner.assert_called(radio_tune_args(radio.state.stations[1]))


def test_prev_station(radio: Radio, runner: TestRunner) -> None:
    radio.prev_station()
    # We're already booted, so we just tune.
    runner.assert_called(radio_tune_args(radio.state.stations[-1]))


def test_pause_next_station(radio: Radio, runner: TestRunner) -> None:
    radio.pause()
    runner.assert_called(radio_pause_args())
    # Since we're paused, this will first boot, then tune.
    radio.next_station()
    runner.assert_called(radio_boot_args())
    runner.assert_called(radio_tune_args(radio.state.stations[1]))

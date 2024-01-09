from __future__ import annotations

from queue import Empty

import pytest

from radiopi.radio import Radio, radio_pause_args
from tests import QueueRunner, running


def test_pause_on_stop(runner: QueueRunner) -> None:
    with running(runner=runner):
        pass
    # On stop, the radio automatically pauses.
    runner.assert_called(radio_pause_args())


def test_pause_on_stop_already_paused(runner: QueueRunner) -> None:
    with running(runner=runner) as radio:
        # Pause the radio.
        radio.pause()
        runner.assert_called(radio_pause_args())
    # On stop, since the radio is already paused, nothing needs to be done.
    with pytest.raises(Empty):
        runner.queue.get_nowait()


def test_state_initial(radio: Radio) -> None:
    # The radio should be playing.
    assert radio.state.playing
    # The stations should be loaded.
    assert radio.state.station_index == 0
    assert len(radio.state.stations) > 0
    # The radio should not be stopping.
    assert not radio.state.stopping

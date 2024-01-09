from __future__ import annotations

from queue import Empty

import pytest

from radiopi import running
from radiopi.radio import radio_boot_args, radio_pause_args, radio_tune_args
from tests import QueueRunner


def test_plays_and_pauses(runner: QueueRunner) -> None:
    with running(pin_factory_name="mock", runner=runner) as radio:
        # On start, the radio automatically boots and tunes.
        runner.assert_called(radio_boot_args())
        runner.assert_called(radio_tune_args(radio.state.stations[0]))
    # On stop, the radio automatically pauses.
    runner.assert_called(radio_pause_args())


def test_does_not_pause_if_paused(runner: QueueRunner) -> None:
    with running(pin_factory_name="mock", runner=runner) as radio:
        # On start, the radio automatically boots and tunes.
        runner.assert_called(radio_boot_args())
        runner.assert_called(radio_tune_args(radio.state.stations[0]))
        # Pause the radio.
        radio.pause()
        runner.assert_called(radio_pause_args())
    # On stop, since the radio is already paused, nothing needs to be done.
    with pytest.raises(Empty):
        runner.queue.get_nowait()

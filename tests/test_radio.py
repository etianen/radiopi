from __future__ import annotations

from queue import Empty

import pytest

from radiopi.radio import Radio, radio_pause_args
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


def test_start_already_started(radio: Radio, runner: TestRunner) -> None:
    pass

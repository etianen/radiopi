from __future__ import annotations

from radiopi import running
from radiopi.radio import radio_boot_args, radio_pause_args, radio_tune_args
from tests import QueueRunner


def test_starts_and_pauses(runner: QueueRunner) -> None:
    with running(pin_factory_name="mock", runner=runner) as radio:
        # On start, the radio automatically boots and tunes.
        runner.assert_called(radio_boot_args())
        runner.assert_called(radio_tune_args(radio.state.stations[0]))
    # On stop, the radio automatically pauses.
    runner.assert_called(radio_pause_args())

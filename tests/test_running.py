from __future__ import annotations

from radiopi import running
from tests import QueueRunner


def test_starts_and_pauses(runner: QueueRunner) -> None:
    with running(pin_factory_name="mock", runner=runner) as radio:
        # On start, the radio automatically boots and tunes.
        runner.assert_radio_booted()
        runner.assert_radio_tuned(radio.state.stations[0])
    # On stop, the radio automatically pauses.
    runner.assert_radio_paused()

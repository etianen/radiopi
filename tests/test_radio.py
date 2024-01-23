from __future__ import annotations

from logot import Logot

from tests import logged, running


def test_running_pause_on_stop(logot: Logot) -> None:
    with running() as radio:
        # On start, the radio will boot and tune.
        logot.wait_for(logged.radio_boot())
        logot.wait_for(logged.radio_tune(radio.state.stations[0]))
    # On stop, the radio automatically pauses.
    logot.wait_for(logged.radio_pause())


def test_running_pause_on_stop_already_paused(logot: Logot) -> None:
    with running() as radio:
        # On start, the radio will boot and tune.
        logot.wait_for(logged.radio_boot())
        logot.wait_for(logged.radio_tune(radio.state.stations[0]))
        # Pause the radio.
        radio.pause()
        logot.wait_for(logged.radio_pause())
    # On stop, since the radio is already paused, nothing needs to be done.
    logot.assert_not_logged(logged.radio_pause())

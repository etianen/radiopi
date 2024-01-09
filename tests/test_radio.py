from __future__ import annotations

from radiopi.radio import Radio


def test_state_initial(radio: Radio) -> None:
    # The radio should be playing.
    assert radio.state.playing
    # The stations should be loaded.
    assert radio.state.station_index == 0
    assert len(radio.state.stations) > 0
    # The radio should not be stopping.
    assert not radio.state.stopping

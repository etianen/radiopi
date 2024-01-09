from __future__ import annotations

from radiopi.radio import Radio
from radiopi.stations import Station


def test_radio_state_initial(radio: Radio) -> None:
    # The radio should be playing.
    assert radio.state.is_playing
    # The stations should be loaded.
    assert radio.state.station_index == 0
    assert len(radio.state.stations) > 0
    assert all(isinstance(station, Station) for station in radio.state.stations)
    # The radio should not be stopping.
    assert not radio.state.stopping

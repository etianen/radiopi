from __future__ import annotations

from radiopi.stations import Station, load_stations


def test_load_stations() -> None:
    stations = load_stations()
    assert stations
    for station in stations:
        assert isinstance(station, Station)

from __future__ import annotations

from radiopi.station import Station, load_stations


def test_load_stations() -> None:
    stations = load_stations()
    assert len(stations) > 0
    assert all(isinstance(station, Station) for station in stations)

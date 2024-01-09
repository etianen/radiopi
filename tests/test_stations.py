from __future__ import annotations

from collections.abc import Sequence

from radiopi.stations import Station


def test_load_stations(stations: Sequence[Station]) -> None:
    # Assert we load at least one station.
    assert stations
    for station in stations:
        assert isinstance(station, Station)


def test_load_stations_unique(stations: Sequence[Station]) -> None:
    # Assert we load a unique set of stations.
    assert len(stations) == len(set(stations))

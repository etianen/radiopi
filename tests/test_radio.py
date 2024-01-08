from __future__ import annotations

from radiopi.radio import Radio


def test_starts_automatically(radio: Radio) -> None:
    assert radio.is_playing


def test_play_idempotent(radio: Radio) -> None:
    radio.play()
    assert radio.is_playing


def test_stop(radio: Radio) -> None:
    radio.stop()
    assert not radio.is_playing


def test_toggle_play(radio: Radio) -> None:
    radio.toggle_play()
    assert not radio.is_playing
    radio.toggle_play()
    assert radio.is_playing


def test_next_prev_station(radio: Radio) -> None:
    station = radio.station
    radio.next_station()
    assert radio.station != station
    radio.prev_station()
    assert radio.station == station

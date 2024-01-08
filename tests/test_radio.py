from __future__ import annotations

from radiopi.radio import Radio


def test_starts_automatically(radio: Radio) -> None:
    assert radio.is_playing

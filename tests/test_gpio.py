from __future__ import annotations

from radiopi.buttons import GPIO
from radiopi.radio import Radio


def test_init(radio: Radio) -> None:
    GPIO(radio)

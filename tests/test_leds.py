from __future__ import annotations

import pytest

from radiopi.leds import fade, pulse


def test_fade() -> None:
    assert [*fade(0.0, 1.0, steps=5, duration=0)] == pytest.approx([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])


def test_pulse() -> None:
    assert [*pulse(0.0, 1.0, steps=5, duration=0)] == pytest.approx(
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
    )

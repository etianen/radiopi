from __future__ import annotations

from gpiozero.pins import Factory

from radiopi.pins import PinFactory


def test_pin_factory(pin_factory: PinFactory) -> None:
    assert isinstance(pin_factory, Factory)

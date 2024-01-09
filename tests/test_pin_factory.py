from __future__ import annotations

from gpiozero.pins import Factory

from radiopi.pin_factory import create_pin_factory


def test_create_pin_factory() -> None:
    pin_factory = create_pin_factory("mock")
    assert isinstance(pin_factory, Factory)

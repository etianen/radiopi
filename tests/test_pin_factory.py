from __future__ import annotations

from gpiozero.pins import Factory

from radiopi.pin_factory import create_pin_factory


def test_create_pin_factory() -> None:
    with create_pin_factory("mock") as pin_factory:
        assert isinstance(pin_factory, Factory)

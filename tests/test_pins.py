from __future__ import annotations

from gpiozero.pins import Factory

from radiopi.pins import PinFactory


def test_create_pin_factory(pin_factory: PinFactory) -> None:
    # Ensure we create a `gpiozero` pin factory.
    assert isinstance(pin_factory, Factory)
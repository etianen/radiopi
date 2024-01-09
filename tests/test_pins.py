from __future__ import annotations

from gpiozero.pins import Factory

from radiopi.pins import PinFactory


def test_create_pin_factory(pin_factory: PinFactory) -> None:
    # Ensure we're creating a `gpiozero` pin factory instance.
    assert isinstance(pin_factory, Factory)

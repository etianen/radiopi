from __future__ import annotations

from collections.abc import Mapping
from contextlib import AbstractContextManager
from pkgutil import resolve_name
from typing import NewType

PinFactory = NewType("PinFactory", object)
PinFactoryName = NewType("PinFactoryName", str)

MOCK_PIN_FACTORY_NAME = PinFactoryName("gpiozero.pins.mock:MockFactory")
RPIGPIO_PIN_FACTORY_NAME = PinFactoryName("gpiozero.pins.rpigpio:RPiGPIOFactory")

PIN_FACTORIES: Mapping[str, PinFactoryName] = {
    "mock": MOCK_PIN_FACTORY_NAME,
    "rpigpio": RPIGPIO_PIN_FACTORY_NAME,
}


def create_pin_factory(pin_factory_name: PinFactoryName) -> AbstractContextManager[PinFactory]:
    pin_factory_cls: type[AbstractContextManager[PinFactory]] = resolve_name(pin_factory_name)
    return pin_factory_cls()

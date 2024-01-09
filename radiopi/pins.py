from __future__ import annotations

from contextlib import AbstractContextManager
from pkgutil import resolve_name
from typing import NewType

PinFactory = NewType("PinFactory", object)
PinFactoryName = NewType("PinFactoryName", str)

PIN_FACTORIES = {
    "mock": PinFactoryName("gpiozero.pins.mock:MockFactory"),
    "rpigpio": PinFactoryName("gpiozero.pins.rpigpio:RPiGPIOFactory"),
}


def create_pin_factory(pin_factory_name: PinFactoryName) -> AbstractContextManager[PinFactory]:
    pin_factory_cls: type[AbstractContextManager[PinFactory]] = resolve_name(pin_factory_name)
    return pin_factory_cls()

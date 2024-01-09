from __future__ import annotations

from contextlib import AbstractContextManager
from pkgutil import resolve_name
from typing import NewType

PinFactory = NewType("PinFactory", object)
PinFactoryFactory = NewType("PinFactoryFactory", str)


PIN_FACTORIES = {
    "mock": PinFactoryFactory("gpiozero.pins.mock:MockFactory"),
    "rpigpio": PinFactoryFactory("gpiozero.pins.rpigpio:RPiGPIOFactory"),
}


def create_pin_factory(name: PinFactoryFactory) -> AbstractContextManager[PinFactory]:
    pin_factory_cls: type[AbstractContextManager[PinFactory]] = resolve_name(PIN_FACTORIES[name])
    return pin_factory_cls()

from __future__ import annotations

from contextlib import AbstractContextManager
from pkgutil import resolve_name
from typing import NewType

PinFactory = NewType("PinFactory", object)

PIN_FACTORIES = {
    "mock": "gpiozero.pins.mock:MockFactory",
    "rpigpio": "gpiozero.pins.rpigpio:RPiGPIOFactory",
}


def create_pin_factory(name: str) -> AbstractContextManager[PinFactory]:
    pin_factory_cls: type[AbstractContextManager[PinFactory]] = resolve_name(PIN_FACTORIES[name])
    return pin_factory_cls()

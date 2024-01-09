from __future__ import annotations

from collections.abc import Mapping
from contextlib import AbstractContextManager
from pkgutil import resolve_name
from typing import Literal, NewType

PinFactory = NewType("PinFactory", object)
PinFactoryName = Literal["mock", "rpigpio"]

PIN_FACTORIES: Mapping[PinFactoryName, str] = {
    "mock": "gpiozero.pins.mock:MockFactory",
    "rpigpio": "gpiozero.pins.rpigpio:RPiGPIOFactory",
}


def create_pin_factory(pin_factory_name: PinFactoryName) -> AbstractContextManager[PinFactory]:
    pin_factory_path = PIN_FACTORIES[pin_factory_name]
    pin_factory_cls: type[AbstractContextManager[PinFactory]] = resolve_name(pin_factory_path)
    return pin_factory_cls()

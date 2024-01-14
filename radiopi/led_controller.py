from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import ClassVar, Literal, final

from gpiozero import PWMLED

from radiopi.log import logger
from radiopi.pin_factory import PinFactory

LEDControllerName = Literal["mock", "pwm"]


class LEDController(ABC):
    transition_duration: ClassVar[float]
    transition_steps: ClassVar[int]

    def __init__(self, pin: int, *, name: str, pin_factory: PinFactory) -> None:
        self.name = name

    @final
    def set_value(self, value: float) -> None:
        logger.debug("LED: %s: Value: %s", self.name, value)
        self._set_value(value)

    @abstractmethod
    def _set_value(self, value: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class MockLEDController(LEDController):
    transition_duration: ClassVar[float] = 0.0
    transition_steps: ClassVar[int] = 1

    def _set_value(self, value: float) -> None:
        pass

    def close(self) -> None:
        pass


class PWMLEDController(LEDController):  # pragma: no cover
    transition_duration: ClassVar[float] = 0.3
    transition_steps: ClassVar[int] = 100

    def __init__(self, pin: int, *, name: str, pin_factory: PinFactory) -> None:
        super().__init__(pin, name=name, pin_factory=pin_factory)
        self.led = PWMLED(pin, pin_factory=pin_factory)

    def _set_value(self, value: float) -> None:
        self.led.value = value

    def close(self) -> None:
        self.led.close()


LED_CONTROLLERS: Mapping[LEDControllerName, type[LEDController]] = {
    "mock": MockLEDController,
    "pwm": PWMLEDController,
}

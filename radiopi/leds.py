from __future__ import annotations

import dataclasses
from abc import abstractmethod
from collections.abc import Generator, Iterable, Mapping
from contextlib import AbstractContextManager, contextmanager
from time import sleep
from types import TracebackType
from typing import Literal

from gpiozero import PWMLED

from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import State, watcher

LEDControllerName = Literal["mock", "pwm"]


class LEDController(AbstractContextManager["LEDController"]):
    @abstractmethod
    def __init__(self, pin: int, *, pin_factory: PinFactory) -> None:
        ...

    @property
    @abstractmethod
    def value(self) -> float:
        raise NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, value: float) -> None:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        pass


class MockLEDController(LEDController):
    def __init__(self, pin: int, *, pin_factory: PinFactory) -> None:
        self._value = 0.0

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value


LED_CONTROLLERS: Mapping[LEDControllerName, type[LEDController]] = {
    "mock": MockLEDController,
    "pwm": PWMLED,
}


@dataclasses.dataclass(frozen=True)
class LEDs:
    play_led: LEDController
    next_station_led: LEDController
    prev_station_led: LEDController


@log_contextmanager(name="Buttons")
@contextmanager
def create_leds(*, led_controller_cls: type[LEDController], pin_factory: PinFactory) -> Generator[LEDs, None, None]:
    with (
        led_controller_cls(13, pin_factory=pin_factory) as play_led,
        led_controller_cls(6, pin_factory=pin_factory) as next_station_led,
        led_controller_cls(5, pin_factory=pin_factory) as prev_station_led,
    ):
        yield LEDs(
            play_led=play_led,
            next_station_led=next_station_led,
            prev_station_led=prev_station_led,
        )


@watcher(name="LEDs")
def leds_watcher(prev_state: State, state: State, *, leds: LEDs) -> None:
    if state.playing:
        # Fade in the LEDs.
        if not prev_state.playing:
            transition(fade(0.0, 1.0), leds.play_led, leds.next_station_led, leds.prev_station_led)
        # Pulse the next station button.
        elif prev_state.station_index % len(prev_state.stations) == state.station_index % len(state.stations) - 1:
            transition(pulse(1.0, 0.0), leds.next_station_led)
        # Pulse the prev station button.
        elif prev_state.station_index % len(prev_state.stations) == state.station_index % len(state.stations) + 1:
            transition(pulse(1.0, 0.0), leds.prev_station_led)
        # Pulse both the station buttons.
        elif prev_state.station != state.station:
            transition(pulse(1.0, 0.0), leds.next_station_led, leds.prev_station_led)
    elif prev_state.playing:
        # Fade out the LEDs.
        transition(fade(1.0, 0.0), leds.play_led, leds.next_station_led, leds.prev_station_led)


def transition(values: Iterable[float], *leds: LEDController) -> None:
    for value in values:
        for led in leds:
            led.value = value


def fade(
    from_value: float,
    to_value: float,
    *,
    steps: int = 100,
    duration: float = 0.3,
) -> Generator[float, None, None]:
    value_interval = (to_value - from_value) / steps
    sleep_interval = duration / steps
    for n in range(steps):
        yield from_value + value_interval * n
        sleep(sleep_interval)
    yield to_value


def pulse(
    from_value: float,
    to_value: float,
    *,
    steps: int = 100,
    duration: float = 0.3,
) -> Generator[float, None, None]:
    yield from fade(from_value, to_value, steps=steps // 2, duration=duration / 2.0)
    yield from fade(to_value, from_value, steps=steps // 2, duration=duration / 2.0)

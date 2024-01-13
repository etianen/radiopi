from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from collections.abc import Generator, Mapping
from contextlib import closing, contextmanager
from time import sleep
from typing import Literal

from gpiozero import PWMLED

from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import State, watcher

LEDControllerName = Literal["mock", "pwm"]


class LEDController(ABC):
    @abstractmethod
    def __init__(self, pin: int, *, pin_factory: PinFactory) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class MockLEDController(LEDController):
    def __init__(self, pin: int, *, pin_factory: PinFactory) -> None:
        pass

    def set_value(self, value: float) -> None:
        pass

    def close(self) -> None:
        pass


class PWMLEDController(LEDController):  # pragma: no cover
    def __init__(self, pin: int, *, pin_factory: PinFactory) -> None:
        self.led = PWMLED(pin, pin_factory=pin_factory)

    def set_value(self, value: float) -> None:
        self.led.value = value

    def close(self) -> None:
        self.led.close()


LED_CONTROLLERS: Mapping[LEDControllerName, type[LEDController]] = {
    "mock": MockLEDController,
    "pwm": PWMLEDController,
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
        closing(led_controller_cls(13, pin_factory=pin_factory)) as play_led,
        closing(led_controller_cls(6, pin_factory=pin_factory)) as next_station_led,
        closing(led_controller_cls(5, pin_factory=pin_factory)) as prev_station_led,
    ):
        yield LEDs(
            play_led=play_led,
            next_station_led=next_station_led,
            prev_station_led=prev_station_led,
        )


@watcher(name="LEDs")
def leds_watcher(prev_state: State, state: State, *, duration: float, leds: LEDs) -> None:
    if state.playing:
        # Fade in the LEDs.
        if not prev_state.playing:
            transition(fade(0.0, 1.0, duration=duration), leds.play_led, leds.next_station_led, leds.prev_station_led)
        # Pulse the play and next station buttons.
        elif prev_state.station_index == state.station_index - 1:
            transition(pulse(1.0, 0.0, duration=duration), leds.play_led, leds.next_station_led)
        # Pulse the play and prev station buttons.
        elif prev_state.station_index == state.station_index + 1:
            transition(pulse(1.0, 0.0, duration=duration), leds.play_led, leds.prev_station_led)
        # Pulse the LEDs.
        elif prev_state.station != state.station:  # pragma: no cover
            transition(pulse(1.0, 0.0, duration=duration), leds.play_led, leds.next_station_led, leds.prev_station_led)
    elif prev_state.playing:
        # Fade out the LEDs.
        transition(fade(1.0, 0.0, duration=duration), leds.play_led, leds.next_station_led, leds.prev_station_led)


def transition(values: Generator[float, None, None], *leds: LEDController) -> None:
    with closing(values):
        for value in values:
            for led in leds:
                led.set_value(value)


def fade(
    from_value: float,
    to_value: float,
    *,
    steps: int = 100,
    duration: float,
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
    duration: float,
) -> Generator[float, None, None]:
    yield from fade(from_value, to_value, steps=steps, duration=duration)
    yield from fade(to_value, from_value, steps=steps, duration=duration)

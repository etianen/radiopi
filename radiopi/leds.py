from __future__ import annotations

import dataclasses
from collections.abc import Generator
from contextlib import contextmanager
from time import sleep

from gpiozero import PWMLED

from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import State, watcher


@dataclasses.dataclass(frozen=True)
class LEDs:
    play_led: PWMLED
    next_station_led: PWMLED
    prev_station_led: PWMLED


@log_contextmanager(name="Buttons")
@contextmanager
def create_leds(*, pin_factory: PinFactory) -> Generator[LEDs, None, None]:
    with (
        PWMLED(1, pin_factory=pin_factory) as play_led,
        PWMLED(2, pin_factory=pin_factory) as next_station_led,
        PWMLED(3, pin_factory=pin_factory) as prev_station_led,
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
            for value in fade(0.0, 1.0):
                leds.play_led.value = value
                leds.next_station_led.value = value
                leds.prev_station_led.value = value
        # Pulse the next station button.
        elif prev_state.station_index % len(prev_state.stations) == state.station_index % len(state.stations) - 1:
            for value in pulse(1.0, 0.0):
                leds.next_station_led.value = value
        # Pulse the prev station button.
        elif prev_state.station_index % len(prev_state.stations) == state.station_index % len(state.stations) + 1:
            for value in pulse(1.0, 0.0):
                leds.prev_station_led.value = value
        # Pulse both the station buttons.
        elif prev_state.station != state.station:
            for value in pulse(1.0, 0.0):
                leds.next_station_led.value = value
                leds.prev_station_led.value = value
    elif prev_state.playing:
        # Fade out the LEDs.
        for leds.play_led.value in fade(1.0, 0.0):
            leds.play_led.value = value
            leds.next_station_led.value = value
            leds.prev_station_led.value = value


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
    yield from fade(to_value, from_value, steps=steps // 2 - 1, duration=duration / 2.0)

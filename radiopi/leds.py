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
def leds(*, pin_factory: PinFactory) -> Generator[LEDs, None, None]:
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
def playing_watcher(prev_state: State, state: State, *, leds: LEDs) -> None:
    if state.playing:
        # Fade in the play button.
        if not prev_state.playing:
            for leds.play_led.value in fade(0.0, 1.0):
                pass
    elif prev_state.playing:
        # Fade out the play button.
        for leds.play_led.value in fade(1.0, 0.0):
            pass


@watcher(name="LEDs")
def station_watcher(prev_state: State, state: State, *, leds: LEDs) -> None:
    if state.playing:
        if not prev_state.playing:
            pass


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

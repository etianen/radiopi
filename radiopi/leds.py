from __future__ import annotations

import dataclasses
from collections.abc import Generator, Sequence
from contextlib import closing, contextmanager
from time import sleep

from radiopi.led_controller import LEDController
from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import State, watcher


@dataclasses.dataclass(frozen=True)
class LEDs:
    play_led: LEDController
    next_station_led: LEDController
    prev_station_led: LEDController

    @property
    def all_leds(self) -> Sequence[LEDController]:
        return (self.play_led, self.next_station_led, self.prev_station_led)


@log_contextmanager(name="Buttons")
@contextmanager
def create_leds(*, led_controller_cls: type[LEDController], pin_factory: PinFactory) -> Generator[LEDs, None, None]:
    with (
        closing(led_controller_cls(13, name="Play", pin_factory=pin_factory)) as play_led,
        closing(led_controller_cls(6, name="Next station", pin_factory=pin_factory)) as next_station_led,
        closing(led_controller_cls(5, name="Prev station", pin_factory=pin_factory)) as prev_station_led,
    ):
        yield LEDs(
            play_led=play_led,
            next_station_led=next_station_led,
            prev_station_led=prev_station_led,
        )


@watcher(name="LEDs")
def leds_watcher(prev_state: State, state: State, *, led_controller_cls: type[LEDController], leds: LEDs) -> None:
    duration = led_controller_cls.transition_duration
    steps = led_controller_cls.transition_steps
    if state.playing:
        # Fade in the LEDs.
        if not prev_state.playing:
            transition(fade(0.0, 1.0, steps=steps), *leds.all_leds, duration=duration)
        # Pulse the play and next station buttons.
        elif prev_state.station_index == state.station_index - 1:
            transition(pulse(1.0, 0.0, steps=steps), leds.play_led, leds.next_station_led, duration=duration)
        # Pulse the play and prev station buttons.
        elif prev_state.station_index == state.station_index + 1:
            transition(pulse(1.0, 0.0, steps=steps), leds.play_led, leds.prev_station_led, duration=duration)
        # Pulse the LEDs.
        elif prev_state.station != state.station:
            transition(pulse(1.0, 0.0, steps=steps), *leds.all_leds, duration=duration)
    elif prev_state.playing:
        # Fade out the LEDs.
        transition(fade(1.0, 0.0, steps=steps), *leds.all_leds, duration=duration)


def transition(values: Sequence[float], *leds: LEDController, duration: float) -> None:
    sleep_interval = duration / len(values)
    for value in values:
        for led in leds:
            led.set_value(value)
        sleep(sleep_interval)


def fade(from_value: float, to_value: float, *, steps: int) -> Sequence[float]:
    return [from_value + ((to_value - from_value) / steps) * n for n in range(steps)] + [to_value]


def pulse(from_value: float, to_value: float, *, steps: int) -> Sequence[float]:
    return [
        *fade(from_value, to_value, steps=steps),
        *fade(to_value, from_value, steps=steps),
    ]

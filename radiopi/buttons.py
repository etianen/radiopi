from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from functools import partial

from gpiozero import Button

from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import Radio
from radiopi.runner import Runner


@log_contextmanager(name="Buttons")
@contextmanager
def create_buttons(*, pin_factory: PinFactory, radio: Radio, runner: Runner) -> Generator[None, None, None]:
    with (
        Button(21, pin_factory=pin_factory) as toggle_play_button,
        Button(16, pin_factory=pin_factory, hold_time=1, hold_repeat=True) as next_station_button,
        Button(12, pin_factory=pin_factory, hold_time=1, hold_repeat=True) as prev_station_button,
        Button(26, pin_factory=pin_factory, hold_time=1, hold_repeat=False) as shutdown_button,
    ):
        # Set event handlers.
        toggle_play_button.when_pressed = radio.toggle_play
        next_station_button.when_pressed = radio.next_station
        next_station_button.when_held = radio.next_station
        prev_station_button.when_pressed = radio.prev_station
        prev_station_button.when_held = radio.prev_station
        shutdown_button.when_held = partial(runner.__call__, ("poweroff", "-h"))
        # All done!
        yield

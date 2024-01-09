from __future__ import annotations

import logging
from collections.abc import Generator
from contextlib import contextmanager

from gpiozero import Button

from radiopi.pins import PinFactory
from radiopi.radio import Radio

logger = logging.getLogger(__name__)


@contextmanager
def buttons(*, pin_factory: PinFactory, radio: Radio) -> Generator[None, None, None]:
    logger.info("Initializing buttons...")
    # Create buttons.
    with (
        Button(21, pin_factory=pin_factory) as toggle_play_button,
        Button(16, pin_factory=pin_factory, hold_time=1, hold_repeat=True) as next_station_button,
        Button(12, pin_factory=pin_factory, hold_time=1, hold_repeat=True) as prev_station_button,
        Button(26, pin_factory=pin_factory, hold_time=1, hold_repeat=False) as shutdown_button,
    ):
        # All done!
        logger.info("Initialized buttons!")
        yield

    # Enable toggle play switch.

    # self._toggle_play_switch.when_pressed = radio.toggle_play
    # Enable next station switch.
    # self._next_station_switch.when_pressed = radio.next_station
    # self._next_station_switch.when_held = radio.next_station
    # Enable previous station switch.
    # self._prev_station_switch.when_pressed = radio.prev_station
    # self._prev_station_switch.when_held = radio.prev_station
    # Enable shutdown switch.
    # self._shutdown_switch.when_held = radio.shutdown
    # All done!

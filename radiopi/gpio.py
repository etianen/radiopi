from __future__ import annotations

import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import NewType

from gpiozero import Button

logger = logging.getLogger(__name__)

PinFactory = NewType("PinFactory", object)


def get_pin_factory() -> PinFactory:
    try:
        # Try to use the real pin factory implementation.
        from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactoryImpl
    except (ImportError, RuntimeError):
        logger.warning("`RPi.GPIO` is not available, using mock pin factory!")
        # Fall back to a mock pin factory implementation.
        # We're either not running on an RPi, or important things are not installed!
        from gpiozero.pins.mock import MockFactory as PinFactoryImpl
    # Create and return the pin factory.
    return PinFactory(PinFactoryImpl())


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

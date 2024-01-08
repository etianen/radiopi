from __future__ import annotations

import logging

from gpiozero import Button, Device  # type: ignore[import-untyped]
from gpiozero.pins.mock import MockFactory  # type: ignore[import-untyped]

from radiopi.radio import Radio

logger = logging.getLogger(__name__)


try:
    # Try to use the real pin factory.
    from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactory  # type: ignore[import-untyped]
except ImportError:
    # Fall back to a mock pin factory.
    # We're either not running on an RPi, or important things are not installed!
    PinFactory = MockFactory


def init_gpio(radio: Radio) -> None:
    logger.info("Initializing GPIO...")
    # Configure `gpiozero`.
    if PinFactory is MockFactory:
        logger.warning("`RPi.GPIO` is not installed, using mock pin factory")
    Device.pin_factory = PinFactory()
    # Enable toggle play switch.
    toggle_play_switch = Button(21)
    toggle_play_switch.when_pressed = radio.toggle_play
    # Enable next station switch.
    next_station_switch = Button(16, hold_time=1, hold_repeat=True)
    next_station_switch.when_pressed = radio.next_station
    next_station_switch.when_held = radio.next_station
    # Enable previous station switch.
    prev_station_switch = Button(12, hold_time=1, hold_repeat=True)
    prev_station_switch.when_pressed = radio.prev_station
    prev_station_switch.when_held = radio.prev_station
    # Enable shutdown switch.
    shutdown_switch = Button(26, hold_time=1, hold_repeat=False)
    shutdown_switch.when_held = radio.shutdown
    # All done!
    logger.info("GPIO initialized!")

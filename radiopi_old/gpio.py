from __future__ import annotations

import logging

from gpiozero import Button, Device

from radiopi.radio import Radio

logger = logging.getLogger(__name__)


try:
    # Try to use the real pin factory.
    from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactory
except (ImportError, RuntimeError):
    logger.warning("`RPi.GPIO` is not available, using mock pin factory!")
    # Fall back to a mock pin factory.
    # We're either not running on an RPi, or important things are not installed!
    from gpiozero.pins.mock import MockFactory as PinFactory


class GPIO:
    def __init__(self, radio: Radio) -> None:
        logger.info("Initializing GPIO...")
        Device.pin_factory = PinFactory()
        # Enable toggle play switch.
        self._toggle_play_switch = Button(21)
        self._toggle_play_switch.when_pressed = radio.toggle_play
        # Enable next station switch.
        self._next_station_switch = Button(16, hold_time=1, hold_repeat=True)
        self._next_station_switch.when_pressed = radio.next_station
        self._next_station_switch.when_held = radio.next_station
        # Enable previous station switch.
        self._prev_station_switch = Button(12, hold_time=1, hold_repeat=True)
        self._prev_station_switch.when_pressed = radio.prev_station
        self._prev_station_switch.when_held = radio.prev_station
        # Enable shutdown switch.
        self._shutdown_switch = Button(26, hold_time=1, hold_repeat=False)
        self._shutdown_switch.when_held = radio.shutdown
        # All done!
        logger.info("GPIO initialized!")

from __future__ import annotations

import logging

from gpiozero import Button, Device

from radiopi.radio import Radio

logger = logging.getLogger(__name__)


try:
    # Try to use the real pin factory.
    from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactory
except ImportError:
    logger.warning("`RPi.GPIO` is not installed, using mock pin factory!")
    # Fall back to a mock pin factory.
    # We're either not running on an RPi, or important things are not installed!
    from gpiozero.pins.mock import MockFactory as PinFactory


class GPIO:
    def __init__(self, radio: Radio) -> None:
        logger.info("Initializing GPIO...")
        Device.pin_factory = PinFactory()
        # Enable toggle play switch.
        self.toggle_play_switch = Button(21)
        self.toggle_play_switch.when_pressed = radio.toggle_play
        # Enable next station switch.
        self.next_station_switch = Button(16, hold_time=1, hold_repeat=True)
        self.next_station_switch.when_pressed = radio.next_station
        self.next_station_switch.when_held = radio.next_station
        # Enable previous station switch.
        self.prev_station_switch = Button(12, hold_time=1, hold_repeat=True)
        self.prev_station_switch.when_pressed = radio.prev_station
        self.prev_station_switch.when_held = radio.prev_station
        # Enable shutdown switch.
        self.shutdown_switch = Button(26, hold_time=1, hold_repeat=False)
        self.shutdown_switch.when_held = radio.shutdown
        # All done!
        logger.info("GPIO initialized!")

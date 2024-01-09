from __future__ import annotations

import logging
from typing import NewType

logger = logging.getLogger(__name__)

PinFactory = NewType("PinFactory", object)


def get_pin_factory() -> PinFactory:
    logger.info("Initializing pin factory...")
    try:
        # Try to use the real pin factory implementation.
        from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactoryImpl
    except (ImportError, RuntimeError):
        logger.warning("`RPi.GPIO` is not available, using mock pin factory!")
        # Fall back to a mock pin factory implementation.
        # We're either not running on an RPi, or important things are not installed!
        from gpiozero.pins.mock import MockFactory as PinFactoryImpl
    # All done!
    pin_factory = PinFactory(PinFactoryImpl())
    logger.info("Initialized pin factory!")
    return pin_factory

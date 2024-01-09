from __future__ import annotations

import logging
from typing import NewType

PinFactory = NewType("PinFactory", object)

logger = logging.getLogger(__name__)


def get_pin_factory() -> PinFactory:
    logger.info("Pin factory: Discovering")
    try:
        # Try to use the real pin factory implementation.
        from gpiozero.pins.rpigpio import RPiGPIOFactory as PinFactoryImpl
    except (ImportError, RuntimeError):
        logger.warning("`RPi.GPIO` is not available, using mock pin factory!")
        # Fall back to a mock pin factory implementation.
        # We're either not running on an RPi, or important things are not installed!
        from gpiozero.pins.mock import MockFactory as PinFactoryImpl
    # All done!
    logger.info("Pin factory: %s: Initializing", PinFactoryImpl.__name__)
    pin_factory = PinFactory(PinFactoryImpl())
    logger.info("Pin factory: %s: Initialized", PinFactoryImpl.__name__)
    return pin_factory

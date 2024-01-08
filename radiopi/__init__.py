from __future__ import annotations

import logging
from signal import pause

from radiopi.gpio import GPIO
from radiopi.radio import Radio


def main() -> None:
    # Configure logging.
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)
    # Initialize radio.
    radio = Radio()
    # Initialize GPIO.
    # We need to keep a reference to this around to prevent the GC closing all `gpiozero` references.
    gpio = GPIO(radio)  # noqa: F841
    # Wait for something to happen.
    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        radio.stop()

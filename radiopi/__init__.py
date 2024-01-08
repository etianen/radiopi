from __future__ import annotations

import logging
from signal import pause

from radiopi.gpio import init_gpio
from radiopi.radio import Radio


def main() -> None:
    # Configure logging.
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)
    # Initialize.
    radio = Radio()
    init_gpio(radio)
    # Wait for something to happen.
    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        radio.stop()

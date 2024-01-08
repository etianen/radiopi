from __future__ import annotations

import logging
from argparse import ArgumentParser
from signal import pause

from radiopi.gpio import init_gpio
from radiopi.radio import Radio


def run(radio: Radio) -> None:
    init_gpio(radio)
    # Wait for something to happen.
    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        radio.stop()


def main() -> None:
    # Create parser.
    parser = ArgumentParser(allow_abbrev=False)
    # Add config args.
    parser.add_argument("--radio-cli-path", default="radio_cli")
    # Parse args.
    args = parser.parse_args()
    # Initialize.
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    radio = Radio(radio_cli_path=args.radio_cli_path)
    del parser
    del args
    # Run.
    run(radio)

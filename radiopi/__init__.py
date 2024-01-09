from __future__ import annotations

import logging
from argparse import ArgumentParser
from collections.abc import Generator
from contextlib import contextmanager
from signal import pause

from radiopi.log import log_contextmanager
from radiopi.pins import PIN_FACTORIES, PinFactoryName, create_pin_factory
from radiopi.radio import Radio, State
from radiopi.stations import load_stations


@log_contextmanager(name="Main")
@contextmanager
def running(
    *,
    pin_factory_name: PinFactoryName,
) -> Generator[Radio, None, None]:
    stations = load_stations()
    state = State(
        is_playing=True,
        station_index=0,
        stations=stations,
        stopping=False,
    )
    radio = Radio(state)
    # Start contexts.
    with (
        create_pin_factory(pin_factory_name) as pin_factory,
    ):
        yield radio


def main() -> None:  # pragma: no cover
    # Parse args.
    parser = ArgumentParser()
    parser.add_argument("--pin-factory", choices=PIN_FACTORIES, default="rpigpio")
    args = parser.parse_args()
    # Run radio.
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    with running(pin_factory_name=args.pin_factory):
        try:
            pause()
        except KeyboardInterrupt:
            pass

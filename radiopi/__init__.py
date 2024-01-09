from __future__ import annotations

from signal import pause

from radiopi.pins import discover_pin_factory
from radiopi.radio import Radio
from radiopi.run import discover_run
from radiopi.stations import load_stations


def main() -> None:  # pragma: no cover
    pin_factory = discover_pin_factory()
    run = discover_run()
    stations = load_stations()
    # Create the radio.
    radio = Radio(
        pin_factory=pin_factory,
        run=run,
        stations=stations,
    )
    # Run the radio.
    with radio.running():
        pause()

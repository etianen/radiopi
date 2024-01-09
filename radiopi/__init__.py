from __future__ import annotations

# import logging
# from signal import pause

# from radiopi.pins import discover_pin_factory
# from radiopi.radio import Radio
# from radiopi.run import discover_run
# from radiopi.stations import load_stations


# def main() -> None:  # pragma: no cover
#     logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
#     pin_factory = discover_pin_factory()
#     run = discover_run()
#     stations = load_stations()
#     # Create radio.
#     radio = Radio(
#         pin_factory=pin_factory,
#         run=run,
#         stations=stations,
#     )
#     # Run radio.
#     with radio.running():
#         try:
#             pause()
#         except KeyboardInterrupt:
#             pass

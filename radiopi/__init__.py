from __future__ import annotations

from argparse import ArgumentParser

from radiopi.run import run
from radiopi.stations import show_stations


def main() -> None:
    # Create parser.
    parser = ArgumentParser(
        allow_abbrev=False,
        description="All we hear is RadioPi...",
    )
    # Create subparsers.
    subparsers = parser.add_subparsers(metavar="COMMAND", required=True)
    # Create the `run` command.
    run_cmd_parser = subparsers.add_parser(
        "run",
        description="Runs the RadioPi control daemon.",
        help="Runs the RadioPi control daemon.",
    )
    run_cmd_parser.set_defaults(cmd=run)
    # Create the `stations` namespace.
    stations_parser = subparsers.add_parser(
        "stations",
        description="Manages the RadioPi station list.",
        help="Manages the RadioPi station list.",
    )
    stations_subparsers = stations_parser.add_subparsers(metavar="COMMAND", required=True)
    # Create the `stations show` command.
    stations_show_cmd_parser = stations_subparsers.add_parser(
        "show",
        description="Shows all stations.",
        help="Shows all stations.",
    )
    stations_show_cmd_parser.set_defaults(cmd=show_stations)
    # Parse args.
    args = vars(parser.parse_args())
    cmd = args.pop("cmd")
    # Run command.
    cmd(**args)

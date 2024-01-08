from __future__ import annotations

from argparse import ArgumentParser

from radiopi.config import Config
from radiopi.run import run
from radiopi.stations import show_stations


def main() -> None:
    """
    All we hear is RadioPi...
    """
    # Create parser.
    parser = ArgumentParser(
        allow_abbrev=False,
        description=main.__doc__,
    )
    # Add config args.
    parser.add_argument(
        "--radio-cli-path",
        default=Config.radio_cli_path,
        help="Path of the DABBoard `radio_cli` binary. This is resolved relative to `$PATH`.",
    )
    parser.add_argument(
        "--stations-list-path",
        default=Config.station_list_path,
        help="Path of the stations list JSON file.",
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
    args = parser.parse_args()
    cmd = args.cmd
    config = Config(
        radio_cli_path=args.radio_cli_path,
        station_list_path=args.stations_list_path,
    )
    del parser
    del args
    # Run command.
    cmd(config)

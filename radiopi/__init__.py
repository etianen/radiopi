from __future__ import annotations

from argparse import ArgumentParser

from radiopi.run import run_cmd


def main() -> None:
    # Create parser.
    parser = ArgumentParser(
        allow_abbrev=False,
        description="All we hear is RadioPi...",
    )
    # Create subparsers.
    subparsers = parser.add_subparsers(metavar="COMMAND", required=True)
    for cmd in (run_cmd,):
        cmd_parser = subparsers.add_parser("run", description=cmd.__doc__, help=cmd.__doc__)
        cmd_parser.set_defaults(cmd=cmd)
    # Parse args.
    args = vars(parser.parse_args())
    cmd = args.pop("cmd")
    # Run command.
    cmd(**args)

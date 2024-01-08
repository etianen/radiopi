from __future__ import annotations

from argparse import ArgumentParser


def main() -> None:
    parser = ArgumentParser(
        description="All we hear is RadioPi...",
        allow_abbrev=False,
    )
    args = parser.parse_args()

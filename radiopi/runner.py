from __future__ import annotations

from collections.abc import Mapping
from subprocess import check_call
from typing import Literal, Protocol

from radiopi.log import logger

RunnerName = Literal["mock", "subprocess"]


class Runner(Protocol):
    def __call__(self, *args: str) -> None:  # pragma: no cover
        ...


def mock_runner(*args: str) -> None:
    logger.info("Runner: Mock: %s", " ".join(args))


def subprocess_runner(*args: str) -> None:
    logger.info("Runner: Subprocess: %s", " ".join(args))
    check_call(args)


RUNNERS: Mapping[RunnerName, Runner] = {
    "mock": mock_runner,
    "subprocess": subprocess_runner,
}

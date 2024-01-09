from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from subprocess import check_call
from typing import Literal, final

from radiopi.log import logger

RunnerName = Literal["mock", "subprocess"]


class Runner(ABC):
    @final
    def __call__(self, *args: str) -> None:  # pragma: no cover
        logger.info("Runner: %s", " ".join(args))
        self._call(args)

    @abstractmethod
    def _call(self, args: Sequence[str]) -> None:
        pass


class MockRunner(Runner):
    def _call(self, args: Sequence[str]) -> None:
        pass


class SubprocessRunner(Runner):
    def _call(self, args: Sequence[str]) -> None:
        check_call(args)


RUNNERS: Mapping[RunnerName, type[Runner]] = {
    "mock": MockRunner,
    "subprocess": SubprocessRunner,
}


def create_runner(runner_name: RunnerName) -> Runner:
    return RUNNERS[runner_name]()

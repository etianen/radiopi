from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from subprocess import check_call
from typing import Literal, final

from typing_extensions import TypeAlias

from radiopi.log import logger

RunnerName = Literal["mock", "subprocess"]

Args: TypeAlias = Sequence[str]


class Runner(ABC):
    @final
    def __call__(self, args: Args) -> None:
        logger.info("Runner: %s", " ".join(args))
        self._call(args)

    @abstractmethod
    def _call(self, args: Args) -> None:
        raise NotImplementedError


class MockRunner(Runner):
    def _call(self, args: Args) -> None:
        pass


class SubprocessRunner(Runner):
    def _call(self, args: Args) -> None:
        check_call(args)


RUNNERS: Mapping[RunnerName, type[Runner]] = {
    "mock": MockRunner,
    "subprocess": SubprocessRunner,
}


def create_runner(runner_name: RunnerName) -> Runner:
    return RUNNERS[runner_name]()

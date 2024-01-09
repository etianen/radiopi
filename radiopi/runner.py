from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from subprocess import check_call
from typing import final

from radiopi.log import logger


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


RUNNERS: Mapping[str, type[Runner]] = {
    "mock": MockRunner,
    "subprocess": SubprocessRunner,
}

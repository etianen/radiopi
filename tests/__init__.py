from __future__ import annotations

import dataclasses
import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager

from radiopi import running as running_
from radiopi.radio import Radio


@contextmanager
def running() -> Generator[Radio, None, None]:
    with running_(
        duration=0.0,
        led_controller_name="mock",
        pin_factory_name="mock",
        runner_name="mock",
    ) as radio:
        yield radio


class ExpectedLog(ABC):
    # Interface.

    @abstractmethod
    def satisfied(self, log: LogMessage) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __or__(self, other: ExpectedLog) -> ExpectedLog:
        return ParallelExpectedLog([self, other])

    def __gt__(self, other: ExpectedLog) -> ExpectedLog:
        return SerialExpectedLog([self, other])


@dataclasses.dataclass()
class LogMessage(ExpectedLog):
    level: int
    message: str

    def satisfied(self, log: LogMessage) -> bool:
        return log == self

    def __str__(self) -> str:  # pragma: no cover
        return f"[{logging.getLevelName(self.level)}] {self.message}"


@dataclasses.dataclass()
class SerialExpectedLog(ExpectedLog):
    expected_logs: list[ExpectedLog]

    def satisfied(self, log: LogMessage) -> bool:
        # If the next expected log is satisfied, remove it.
        if self.expected_logs[0].satisfied(log):
            self.expected_logs.pop(0)
        # If there are no more expected logs, we're satisfied.
        return not self.expected_logs

    def __str__(self) -> str:  # pragma: no cover
        return f"({' > '.join(map(str, self.expected_logs))})"


@dataclasses.dataclass()
class ParallelExpectedLog(ExpectedLog):
    expected_logs: list[ExpectedLog]

    def satisfied(self, log: LogMessage) -> bool:
        # If the any expected log is satisfied, remove it.
        self.expected_logs = [expected_log for expected_log in self.expected_logs if not expected_log.satisfied(log)]
        # If there are no more expected logs, we're satisfied.
        return not self.expected_logs

    def __str__(self) -> str:  # pragma: no cover
        return f"({' | '.join(map(str, self.expected_logs))})"

from __future__ import annotations

import dataclasses
import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from queue import Empty, SimpleQueue

from radiopi import running as running_
from radiopi.radio import Radio
from radiopi.runner import Args


@contextmanager
def running() -> Generator[Radio, None, None]:
    with running_(
        duration=0.0,
        led_controller_name="mock",
        pin_factory_name="mock",
        runner_name="mock",
    ) as radio:
        yield radio


class AwaitLog(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: SimpleQueue[logging.LogRecord] = SimpleQueue()

    def emit(self, record: logging.LogRecord) -> None:
        self.records.put(record)

    def __call__(self, expected_log: ExpectedLog) -> None:
        # Wait for all message groups to be satisfied.
        while True:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                raise AssertionError(f"Did not log:\n\n{expected_log}")
            # Check the log record.
            if expected_log.satisfied(LogMessage(level=record.levelno, message=record.getMessage())):
                return


class ExpectedLog(ABC):
    @classmethod
    def runner_call(cls, args: Args) -> ExpectedLog:
        return LogMessage(level=logging.INFO, message=f"Runner: {' '.join(args)}")

    @classmethod
    def led_value(cls, name: str, value: float) -> ExpectedLog:
        return LogMessage(level=logging.DEBUG, message=f"LED: {name}: Value: {value}")

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
        if self.expected_logs[0].satisfied(log):
            self.expected_logs.pop(0)
        return bool(self.expected_logs)

    def __str__(self) -> str:  # pragma: no cover
        return "\n".join(map(str, self.expected_logs))


@dataclasses.dataclass()
class ParallelExpectedLog(ExpectedLog):
    expected_logs: list[ExpectedLog]

    def satisfied(self, log: LogMessage) -> bool:
        self.expected_logs = [expected_log for expected_log in self.expected_logs if not expected_log.satisfied(log)]
        return bool(self.expected_logs)

    def __str__(self) -> str:  # pragma: no cover
        return " | ".join(map(str, self.expected_logs))

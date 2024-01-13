from __future__ import annotations

import dataclasses
import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from queue import Empty, SimpleQueue

from radiopi import running as running_
from radiopi.radio import Radio, radio_boot_args, radio_pause_args, radio_tune_args
from radiopi.runner import Args
from radiopi.station import Station


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
        self.records: SimpleQueue[LogMessage] = SimpleQueue()

    def emit(self, record: logging.LogRecord) -> None:
        self.records.put(LogMessage(level=record.levelno, message=record.getMessage()))

    def __call__(self, expected_log: ExpectedLog) -> None:
        # Wait for all message groups to be satisfied.
        while True:
            # Wait for a log record.
            try:
                log_message = self.records.get(timeout=0.1)
            except Empty:
                raise AssertionError(f"Did not log:\n\n{expected_log}") from None
            # Check the log record.
            if expected_log.satisfied(log_message):
                return


class ExpectedLog(ABC):
    # Runner helpers.

    @classmethod
    def runner_call(cls, args: Args) -> ExpectedLog:
        return LogMessage(level=logging.INFO, message=f"Runner: {' '.join(args)}")

    # LED helpers.

    @classmethod
    def led_value(cls, name: str, value: float) -> ExpectedLog:
        return LogMessage(level=logging.DEBUG, message=f"LED: {name}: Value: {value}")

    @classmethod
    def led_fade(cls, name: str, from_value: float, to_value: float) -> ExpectedLog:
        return cls.led_value(name, to_value)

    # Radio helpers.

    @classmethod
    def radio_boot(cls) -> ExpectedLog:
        return (
            cls.runner_call(radio_boot_args())
            | cls.led_value("Play", 1.0)
            | cls.led_value("Next station", 1.0)
            | cls.led_value("Prev station", 1.0)
        )

    @classmethod
    def radio_tune(cls, station: Station) -> ExpectedLog:
        return cls.runner_call(radio_tune_args(station))

    @classmethod
    def radio_pause(cls) -> ExpectedLog:
        return (
            cls.runner_call(radio_pause_args())
            | cls.led_value("Play", 0.0)
            | cls.led_value("Next station", 0.0)
            | cls.led_value("Prev station", 0.0)
        )

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
        if self.expected_logs[0].satisfied(log):
            self.expected_logs.pop(0)
        return not self.expected_logs

    def __str__(self) -> str:  # pragma: no cover
        return "\n".join(map(str, self.expected_logs))


@dataclasses.dataclass()
class ParallelExpectedLog(ExpectedLog):
    expected_logs: list[ExpectedLog]

    def satisfied(self, log: LogMessage) -> bool:
        self.expected_logs = [expected_log for expected_log in self.expected_logs if not expected_log.satisfied(log)]
        return not self.expected_logs

    def __str__(self) -> str:  # pragma: no cover
        return " | ".join(map(str, self.expected_logs))

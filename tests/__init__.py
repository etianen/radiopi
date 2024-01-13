from __future__ import annotations

import dataclasses
import logging
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

    def __call__(self, *expected_logs: ExpectedLog) -> None:
        expected_logs = set(expected_logs)
        # Wait for all message groups to be satisfied.
        while expected_logs:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                message_groups_str = "\n".join(map(str, expected_logs))
                raise AssertionError(f"Did not log:\n\n{message_groups_str}")
            # Check the log record.
            record_log = ExpectedLog(level=record.levelno, message=record.getMessage())
            if record_log in expected_logs:
                expected_logs.remove(record_log)


@dataclasses.dataclass(frozen=True)
class ExpectedLog:
    level: int
    message: str

    @classmethod
    def runner_call(cls, args: Args) -> ExpectedLog:
        return ExpectedLog(level=logging.INFO, message=f"Runner: {' '.join(args)}")

    @classmethod
    def led_value(cls, name: str, value: float) -> ExpectedLog:
        return ExpectedLog(level=logging.DEBUG, message=f"LED: {name}: Value: {value}")

    def __str__(self) -> str:
        return f"[{logging.getLevelName(self.level)}] {self.message}"

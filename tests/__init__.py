from __future__ import annotations

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

    def assert_runner_called(self, args: Args) -> None:
        self(f"[INFO] Runner: {' '.join(args)}")

    def assert_led_value(self, name: str, value: float) -> None:
        self(f"[DEBUG] LED: {name}: Value: {value}")

    def __call__(self, message: str) -> None:
        while True:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                raise AssertionError(f"Did not log: {message}")
            # Check the log record.
            if f"[{logging.getLevelName(record.levelno)}] {record.getMessage()}" == message:
                break

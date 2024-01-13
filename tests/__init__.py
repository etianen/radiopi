from __future__ import annotations

import logging
from collections.abc import Generator, Mapping
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
        self(logging.INFO, f"Runner: {' '.join(args)}")

    def assert_led_value(self, name: str, value: float) -> None:
        self(logging.DEBUG, f"LED: {name}: Value: {value}")

    def __call__(self, level: int, message: str, /, extra: Mapping[str, object] | None = None) -> None:
        while True:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                raise AssertionError(f"Did not log: [{logging.getLevelName(level)}] {message}")
            # Check the log record.
            if record.levelno == level and record.getMessage() == message:
                break

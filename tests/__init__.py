from __future__ import annotations

import logging
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from queue import Empty, SimpleQueue

from radiopi import running as running_
from radiopi.leds import MockLEDController
from radiopi.radio import Radio
from radiopi.runner import Args


@contextmanager
def running() -> Generator[Radio, None, None]:
    with running_(
        duration=0.0,
        led_controller_cls=MockLEDController,
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
        self(logging.INFO, "Runner:", extra={"radiopi.runner.args": args})

    def __call__(self, level: int, message: str, /, extra: Mapping[str, object] | None = None) -> None:
        while True:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                extra_str = f" {extra!r}" if extra else ""
                raise AssertionError(f"Did not log: [{logging.getLevelName(level)}] {message}{extra_str}")
            # Check the log record.
            if (
                record.levelno == level
                and record.getMessage().startswith(message)
                and (extra is None or all(getattr(record, key, object()) == value for key, value in extra.items()))
            ):
                break

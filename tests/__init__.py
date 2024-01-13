from __future__ import annotations

import logging
from collections.abc import Generator
from contextlib import contextmanager
from itertools import chain
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

    def __call__(self, *messages: str | tuple[str]) -> None:
        # Normalize message groups.
        message_groups: list[set[str]] = [set((m,) if isinstance(m, str) else m) for m in messages]
        # Wait for all message groups to be satisfied.
        while message_groups:
            # Wait for a log record.
            try:
                record = self.records.get(timeout=0.1)
            except Empty:
                message_groups_str = "\n".join(chain.from_iterable(message_groups))
                raise AssertionError(f"Did not log:\n\n{message_groups_str}")
            # Check the log record.
            record_str = f"[{logging.getLevelName(record.levelno)}] {record.getMessage()}"
            if record_str in message_groups[0]:
                message_groups[0].remove(record_str)
                if not message_groups[0]:
                    message_groups.pop(0)

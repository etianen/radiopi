from __future__ import annotations

from collections.abc import Mapping, Sequence
from queue import SimpleQueue

from radiopi.runner import Runner


class QueueRunner(Runner):
    def __init__(self) -> None:
        self.queue: SimpleQueue[Sequence[str]] = SimpleQueue()

    def _call(self, args: Sequence[str]) -> None:
        self.queue.put_nowait(args)

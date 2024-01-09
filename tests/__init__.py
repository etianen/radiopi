from __future__ import annotations

from collections.abc import Sequence
from queue import SimpleQueue

from radiopi.runner import Runner
from radiopi.station import Station


class QueueRunner(Runner):
    def __init__(self) -> None:
        self.queue: SimpleQueue[Sequence[str]] = SimpleQueue()

    def _call(self, args: Sequence[str]) -> None:
        self.queue.put_nowait(args)

    def assert_called(self, *expected_args: str) -> None:
        args = self.queue.get(timeout=1.0)
        assert args == expected_args

    def assert_booted(self) -> None:
        self.assert_called("radio_cli", "--boot=D")

    def assert_tuned(self, station: Station) -> None:
        self.assert_called(
            "radio_cli",
            f"--component={station.component_id}",
            f"--service={station.service_id}",
            f"--frequency={station.frequency_index}",
            "--play",
            "--level=63",
        )

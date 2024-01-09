from __future__ import annotations

import dataclasses

from radiopi.subprocess import Run


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int


class Radio:
    def __init__(self, *, run: Run) -> None:
        self._run = run

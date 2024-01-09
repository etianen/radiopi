from __future__ import annotations

import dataclasses
from collections.abc import Generator
from threading import Condition

from radiopi.subprocess import Run


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int


class Radio:
    def __init__(self, *, run: Run) -> None:
        self._run = run
        self._state = State(is_playing=False, station_index=0)
        self._condition = Condition()
        self._stopping = False

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        with self._condition:
            if state != self._state:
                # Update the state and notify listeners.
                self._state = state
                self._condition.notify()

    def running(self) -> Generator[Radio, None, None]:
        yield self

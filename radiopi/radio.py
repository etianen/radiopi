from __future__ import annotations

import dataclasses
import logging
from collections.abc import Sequence
from threading import Condition

from radiopi.stations import Station

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int
    stations: Sequence[Station]
    stopping: bool

    @property
    def station(self) -> Station:
        return self.stations[self.station_index % len(self.stations)]


class Radio:
    def __init__(self, state: State) -> None:
        self._state = state
        self._condition = Condition()

    @property
    def state(self) -> State:
        return self._state

    def _set_state(self, state: State) -> None:
        self._state = state
        self._condition.notify()

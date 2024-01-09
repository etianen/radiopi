from __future__ import annotations

import dataclasses
import logging
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from threading import Condition

from radiopi.pins import PinFactory
from radiopi.stations import Station, load_stations
from radiopi.subprocess import Run

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int
    stations: Sequence[Station]


class Radio:
    def __init__(self, *, pin_factory: PinFactory, run: Run) -> None:
        self._pin_factory = pin_factory
        self._run = run
        # Initialize state.
        self._condition = Condition()
        self._state = State(
            is_playing=False,
            station_index=0,
            stations=load_stations(),
        )
        self._stopping = False

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        with self._condition:
            if state != self._state:
                # Update the state and notify listeners.
                logger.debug("State updated: %r", state)
                self._state = state
                self._condition.notify()

    @contextmanager
    def running(self) -> Generator[Radio, None, None]:
        yield self

    @contextmanager
    def _initializing_buttons(self) -> Generator[None, None, None]:
        yield

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from threading import Condition

from gpiozero import Button

from radiopi.pins import PinFactory
from radiopi.stations import Station
from radiopi.subprocess import Run

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int
    stations: Sequence[Station]


class Radio:
    def __init__(self, *, pin_factory: PinFactory, run: Run, stations: Sequence[Station]) -> None:
        self._pin_factory = pin_factory
        self._run = run
        # Initialize state.
        self._condition = Condition()
        self._state = State(
            is_playing=False,
            station_index=0,
            stations=stations,
        )
        self._stopping = False

    # State.

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        with self._condition:
            if state != self._state:
                # Update the state and notify listeners.
                logger.debug("State: Update: %r", state)
                self._state = state
                self._condition.notify()

    # Context.

    @contextmanager
    def running(self) -> Generator[Radio, None, None]:
        with self._initializing_buttons():
            yield self

    @contextmanager
    def _initializing_buttons(self) -> Generator[None, None, None]:
        logger.info("Buttons: Initalizing")
        with (
            Button(21, pin_factory=self._pin_factory) as toggle_play_button,
            Button(16, pin_factory=self._pin_factory, hold_time=1, hold_repeat=True) as next_station_button,
            Button(12, pin_factory=self._pin_factory, hold_time=1, hold_repeat=True) as prev_station_button,
            Button(26, pin_factory=self._pin_factory, hold_time=1, hold_repeat=False) as shutdown_button,
        ):
            # All done!
            logger.info("Buttons: Initalized")
            yield

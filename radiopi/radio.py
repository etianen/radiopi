from __future__ import annotations

import dataclasses
from collections.abc import Callable, Generator, Sequence
from contextlib import AbstractContextManager
from functools import wraps
from threading import Condition

from typing_extensions import Concatenate, ParamSpec, TypeAlias

from radiopi.daemons import daemon
from radiopi.log import logger
from radiopi.stations import Station

P = ParamSpec("P")


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
        logger.info("Radio: State: Set: %r", state)
        self._state = state
        self._condition.notify()


WatcherCallable: TypeAlias = Callable[Concatenate[State, State, P], None]
WatcherContextManagerCallable: TypeAlias = Callable[Concatenate[Radio, P], AbstractContextManager[None]]


def watcher(*, name: str) -> Callable[[WatcherCallable[P]], WatcherContextManagerCallable[P]]:
    def decorator(fn: WatcherCallable[P]) -> WatcherContextManagerCallable[P]:
        @wraps(fn)
        @daemon(name=name)
        def watcher_wrapper(radio: Radio, /, *args: P.args, **kwargs: P.kwargs) -> None:
            pass

        return watcher_wrapper

    return decorator

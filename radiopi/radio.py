from __future__ import annotations

import dataclasses
from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from functools import wraps
from threading import Condition
from typing import Optional

from typing_extensions import Concatenate, ParamSpec, TypeAlias

from radiopi.daemon import daemon
from radiopi.log import logger
from radiopi.runner import Runner
from radiopi.station import Station

P = ParamSpec("P")


@dataclasses.dataclass(frozen=True)
class State:
    playing: bool
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
        logger.debug("Radio: State: Set: %r", state)
        self._state = state
        self._condition.notify()

    def stop(self) -> None:
        with self._condition:
            self._set_state(dataclasses.replace(self._state, stopping=True))


WatcherCallable: TypeAlias = Callable[Concatenate[Optional[State], State, P], None]
WatcherContextManagerCallable: TypeAlias = Callable[Concatenate[Radio, P], AbstractContextManager[None]]


def watcher(*, name: str) -> Callable[[WatcherCallable[P]], WatcherContextManagerCallable[P]]:
    def decorator(fn: WatcherCallable[P]) -> WatcherContextManagerCallable[P]:
        @wraps(fn)
        @daemon(name=name)
        def watcher_wrapper(radio: Radio, /, *args: P.args, **kwargs: P.kwargs) -> None:
            prev_state: State | None = None
            while True:
                # Wait for a state change.
                with radio._condition:
                    while radio._state == prev_state:
                        radio._condition.wait()
                    state = radio._state
                # Call the state watcher.
                fn(prev_state, state, *args, **kwargs)
                prev_state = state
                # Possibly stop.
                if state.stopping:
                    break

        return watcher_wrapper

    return decorator


@watcher(name="Radio")
def radio_watcher(prev_state: State | None, state: State, runner: Runner) -> None:
    pass

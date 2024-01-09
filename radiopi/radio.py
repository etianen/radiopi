from __future__ import annotations

import dataclasses
import logging
from collections.abc import Callable, Generator, Sequence
from contextlib import contextmanager
from threading import Condition, Thread

from gpiozero import Button

from radiopi.pins import PinFactory
from radiopi.run import Run
from radiopi.stations import Station

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int
    stations: Sequence[Station]

    @property
    def station(self) -> Station:
        return self.stations[self.station_index % len(self.stations)]


class Radio:
    def __init__(self, *, pin_factory: PinFactory, run: Run, stations: Sequence[Station]) -> None:
        self._pin_factory = pin_factory
        self._run = run
        # Initialize state.
        self._condition = Condition()
        self._stopping = False
        self._state = State(
            is_playing=False,
            station_index=0,
            stations=stations,
        )

    # State.

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        # Set state and notify listeners.
        logger.debug("State: Set: %r", state)
        self._state = state
        self._condition.notify_all()

    # Context.

    @contextmanager
    def running(self) -> Generator[Radio, None, None]:
        logger.info("Main: Running")
        with (
            self._running_thread(self._radio_target, name="Radio"),
            self._initializing_buttons(),
        ):
            try:
                yield self
            finally:
                # Notify stopping.
                logger.info("Main: Stopping")
                with self._condition:
                    self._stopping = True
                    self.state = dataclasses.replace(self.state, is_playing=False)
        # All done!
        logger.info("Main: Stopped")

    @contextmanager
    def _running_thread(self, target: Callable[[], None], name: str) -> Generator[None, None, None]:
        # Create thread.
        logger.info("Thread: %s: Starting", name)
        thread = Thread(target=target, name=name, daemon=True)
        thread.start()
        try:
            # All done!
            logger.info("Thread: %s: Started", name)
            yield
        finally:
            # Stop thread.
            logger.info("Thread: %s: Stopping", name)
            thread.join(timeout=10.0)
            if thread.is_alive():  # pragma: no cover
                logger.error("Thread: %s: Zombie", name)
            else:
                logger.info("Thread: %s: Stopped", name)

    @contextmanager
    def _initializing_buttons(self) -> Generator[None, None, None]:
        # Create buttons.
        logger.info("Buttons: Initalizing")
        with (
            Button(21, pin_factory=self._pin_factory) as toggle_play_button,
            Button(16, pin_factory=self._pin_factory, hold_time=1, hold_repeat=True) as next_station_button,
            Button(12, pin_factory=self._pin_factory, hold_time=1, hold_repeat=True) as prev_station_button,
            Button(26, pin_factory=self._pin_factory, hold_time=1, hold_repeat=False) as shutdown_button,
        ):
            # Set event handlers.
            toggle_play_button.when_pressed = self.on_toggle_play
            next_station_button.when_pressed = self.on_next_station
            next_station_button.when_held = self.on_next_station
            prev_station_button.when_pressed = self.on_prev_station
            prev_station_button.when_held = self.on_prev_station
            shutdown_button.when_held = self.on_shutdown
            # All done!
            logger.info("Buttons: Initialized")
            yield

    # Thread targets.

    def _radio_target(self) -> None:
        prev_state = self.state
        while not self._stopping:
            # Wait for notify.
            with self._condition:
                while True:
                    # Grab the new state.
                    state = self.state
                    if (
                        self._stopping
                        or state.is_playing != prev_state.is_playing
                        or state.station_index != prev_state.station_index
                    ):
                        break
                    # Wait for notify.
                    self._condition.wait()
            # Handle new state.
            if state.is_playing:
                # Tune radio.
                station = state.station
                logger.info("Radio: Tuning: %r", station)
                self._run(
                    (
                        "radio_cli",
                        "--boot=D",
                        f"--component={station.component_id}",
                        f"--service={station.service_id}",
                        f"--frequency={station.frequency_index}",
                        "--play",
                        "--level=63",
                    )
                )
                logger.info("Radio: Playing: %r", station)
            else:
                # Shutdown radio.
                logger.info("Radio: Shutting down")
                self._run(("radio_cli", "--shutdown"))
                logger.info("Radio: Shutdown")

    # Event handlers.

    def on_toggle_play(self) -> None:
        with self._condition:
            state = self.state
            self.state = dataclasses.replace(state, is_playing=not state.is_playing)

    def on_next_station(self) -> None:
        with self._condition:
            state = self.state
            self.state = dataclasses.replace(state, is_playing=True, station_index=state.station_index + 1)

    def on_prev_station(self) -> None:
        with self._condition:
            state = self.state
            self.state = dataclasses.replace(state, is_playing=True, station_index=state.station_index - 1)

    def on_shutdown(self) -> None:
        self._run(("poweroff", "-h"))

from __future__ import annotations

import logging
import subprocess
from collections.abc import Callable, Sequence
from functools import wraps
from shutil import which
from threading import RLock
from typing import Any, TypeVar

from radiopi.stations import Station, load_stations

C = TypeVar("C", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def _locked(fn: C) -> C:
    @wraps(fn)
    def _locked_wrapper(self: Radio, *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            return fn(self, *args, **kwargs)

    return _locked_wrapper  # type: ignore[return-value]


class Radio:
    def __init__(self) -> None:
        logger.info("Hello RadioPi!")
        self._lock = RLock()
        # See if `radio_cli` is installed.
        self._radio_cli_path = which("radio_cli")
        if self._radio_cli_path is None:
            logger.warning("`radio_cli` is not installed, using mock radio CLI!")
        # Load all stations.
        self.stations: Sequence[Station] = load_stations()
        self._station_index: int = 0
        # Start the radio.
        self._is_playing = False
        self.play()

    def _cli(self, *args: str) -> None:
        logger.debug("Running `radio_cli`: %r", args)
        if self._radio_cli_path is not None:
            subprocess.check_call((self._radio_cli_path, *args))

    @_locked
    def play(self) -> None:
        # Boot, if not playing.
        if not self._is_playing:
            logger.info("Booting radio...")
            self._cli("--boot=D")
            self._is_playing = True
            logger.info("Radio booted!")
        # Tune to the station.
        station: Station = self.stations[self._station_index % len(self.stations)]
        logger.info(f"Tuning to {station.label}...")
        self._cli(
            f"--component={station.component_id}",
            f"--service={station.service_id}",
            f"--frequency={station.frequency_index}",
            "--play",
            "--level=63",
        )
        logger.info(f"Playing {station.label}!")

    @_locked
    def stop(self) -> None:
        # Shutdown, if playing.
        if self._is_playing:
            logger.info("Shutting down radio...")
            self._cli("--shutdown")
            self._is_playing = False
            logger.info("Radio shutdown!")

    @_locked
    def toggle_play(self) -> None:
        if self._is_playing:
            self.stop()
        else:
            self.play()

    @_locked
    def next_station(self) -> None:
        self._station_index += 1
        self.play()

    @_locked
    def prev_station(self) -> None:
        self._station_index -= 1
        self.play()

    @_locked
    def shutdown(self) -> None:
        self.stop()
        logger.info("Goodby RadioPi...")
        subprocess.check_call(["poweroff", "-h"])

from __future__ import annotations

import logging
import subprocess
from shutil import which

from radiopi.stations import Station, load_stations

logger = logging.getLogger(__name__)


class Radio:
    def __init__(self) -> None:
        logger.info("Hello RadioPi!")
        # See if `radio_cli` is installed.
        self.radio_cli_path = which("radio_cli")
        if self.radio_cli_path is None:
            logger.warning("`radio_cli` is not installed, using mock CLI")
        # Load all stations.
        self.stations: list[Station] = load_stations()
        self.station_index: int = 0
        # Start the radio.
        self.is_playing = False
        self.toggle_play()

    def cli(self, *args: str) -> None:
        logger.debug("Running `radio_cli`: %r", args)
        if self.radio_cli_path is not None:
            subprocess.check_call((self.radio_cli_path, *args))

    def play(self) -> None:
        # Boot, if not playing.
        if not self.is_playing:
            logger.info("Booting radio...")
            self.cli("--boot=D")
            self.is_playing = True
            logger.info("Radio booted!")
        # Tune to the station.
        station: Station = self.stations[self.station_index % len(self.stations)]
        logger.info(f"Tuning to {station.label}...")
        self.cli(
            f"--component={station.component_id}",
            f"--service={station.service_id}",
            f"--frequency={station.frequency_index}",
            "--play",
            "--level=63",
        )
        logger.info(f"Playing {station.label}!")

    def stop(self) -> None:
        # Shutdown, if playing.
        if self.is_playing:
            logger.info("Shutting down radio...")
            self.cli("--shutdown")
            self.is_playing = False
            logger.info("Radio shutdown!")

    def toggle_play(self) -> None:
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def next_station(self) -> None:
        self.station_index += 1
        self.play()

    def prev_station(self) -> None:
        self.station_index -= 1
        self.play()

    def shutdown(self) -> None:
        self.stop()
        logger.info("Goodby RadioPi...")
        subprocess.check_call(["poweroff", "-h"])

from __future__ import annotations

import logging
import subprocess

from radiopi.stations import Station, load_stations

logger = logging.getLogger(__name__)


class Radio:
    def __init__(self, *, radio_cli_path: str) -> None:
        self.radio_cli_path = radio_cli_path
        self.is_playing = False
        # Load all stations.
        self.stations: list[Station] = load_stations()
        self.station_index: int = 0
        # Start the radio.
        self.console.print("[green bold]Hello RadioPI![/]")
        self.toggle_play()

    def cli(self, *args: str) -> None:
        subprocess.check_call((RADIO_CLI, *args))

    def play(self) -> None:
        # Boot, if not playing.
        if not self.is_playing:
            self.console.print("[cyan]Booting radio...[/]")
            self.cli("--boot=D")
            self.is_playing = True
            self.console.print("[green]Radio booted![/]")
        # Tune to the station.
        station: Station = self.stations[self.station_index % len(self.stations)]
        self.console.print(f"Tuning to [cyan]{station.label}[/]...")
        self.console.print(station)
        self.cli(
            f"--component={station.component_id}",
            f"--service={station.service_id}",
            f"--frequency={station.frequency_index}",
            "--play",
            "--level=63",
        )
        self.console.print(f"Playing [green]{station.label}[/]!")

    def stop(self) -> None:
        # Shutdown, if playing.
        if self.is_playing:
            self.console.print("[cyan]Shutting down radio...[/]")
            self.cli("--shutdown")
            self.is_playing = False
            self.console.print("[red]Radio shutdown![/]")

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
        self.console.print("[cyan bold]Goodby RadioPi...[/]")
        subprocess.check_call(["poweroff", "-h"])

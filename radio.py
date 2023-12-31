from __future__ import annotations

import subprocess
from signal import pause

from gpiozero import Button, Device  # type: ignore[import-untyped]
from gpiozero.pins.rpigpio import RPiGPIOFactory  # type: ignore[import-untyped]
from rich.console import Console

from stations import Station, load_stations

RADIO_CLI = "/opt/DABBoard/radio_cli_v3.1.0"


class Radio:
    def __init__(self) -> None:
        self.console = Console()
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


def main():
    radio = Radio()
    # Configure `gpiozero`.
    Device.pin_factory = RPiGPIOFactory()
    # Enable toggle play switch.
    toggle_play_switch = Button(21)
    toggle_play_switch.when_pressed = radio.toggle_play
    # Enable next station switch.
    next_station_switch = Button(16, hold_time=1, hold_repeat=True)
    next_station_switch.when_pressed = radio.next_station
    next_station_switch.when_held = radio.next_station
    # Enable previous station switch.
    prev_station_switch = Button(12, hold_time=1, hold_repeat=True)
    prev_station_switch.when_pressed = radio.prev_station
    prev_station_switch.when_held = radio.prev_station
    # Enable shutdown switch.
    shutdown_switch = Button(26, hold_time=1, hold_repeat=False)
    shutdown_switch.when_held = radio.shutdown
    # Wait for something to happen.
    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        radio.stop()


if __name__ == "__main__":
    main()

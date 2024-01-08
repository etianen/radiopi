from __future__ import annotations

from signal import pause

from gpiozero import Button, Device  # type: ignore[import-untyped]
from gpiozero.pins.rpigpio import RPiGPIOFactory  # type: ignore[import-untyped]

from radiopi.gpio import init_gpio
from radiopi.radio import Radio
from radiopi.stations import Station, load_stations


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

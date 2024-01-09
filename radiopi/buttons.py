from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from radiopi.log import log_contextmanager
from radiopi.pin_factory import PinFactory
from radiopi.radio import Radio


@log_contextmanager(name="Buttons")
@contextmanager
def buttons(*, pin_factory: PinFactory, radio: Radio) -> Generator[None, None, None]:
    with (
        Button(21) as toggle_play_button,
        Button(16, hold_time=1, hold_repeat=True) as next_station_button,
        Button(12, hold_time=1, hold_repeat=True) as prev_station_button,
        Button(26, hold_time=1, hold_repeat=False) as shutdown_button,
    ):


    # Enable toggle play switch.
    self._toggle_play_switch =
    self._toggle_play_switch.when_pressed = radio.toggle_play
    # Enable next station switch.
    self._next_station_switch =
    self._next_station_switch.when_pressed = radio.next_station
    self._next_station_switch.when_held = radio.next_station
    # Enable previous station switch.
    self._prev_station_switch =
    self._prev_station_switch.when_pressed = radio.prev_station
    self._prev_station_switch.when_held = radio.prev_station
    # Enable shutdown switch.
    self._shutdown_switch = Button(26, hold_time=1, hold_repeat=False)
    self._shutdown_switch.when_held = radio.shutdown

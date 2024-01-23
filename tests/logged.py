from __future__ import annotations

from logot import Logged, logged

from radiopi.radio import radio_boot_args, radio_pause_args, radio_tune_args
from radiopi.runner import Args
from radiopi.station import Station

# Runner helpers.


def runner_call(args: Args) -> Logged:
    return logged.info(f"Runner: {' '.join(args)}")


# LED helpers.


def led_value(name: str, value: float) -> Logged:
    return logged.debug(f"LED: {name}: Value: {value}")


def led_fade(name: str, from_value: float, to_value: float) -> Logged:
    return led_value(name, from_value) >> led_value(name, to_value)


def led_pulse(name: str, from_value: float, to_value: float) -> Logged:
    return led_fade(name, from_value, to_value) >> led_fade(name, to_value, from_value)


# Radio helpers.


def radio_boot() -> Logged:
    return runner_call(radio_boot_args())


def radio_tune(station: Station) -> Logged:
    return runner_call(radio_tune_args(station))


def radio_pause() -> Logged:
    return runner_call(radio_pause_args())


# UX helpers.


def ux_tune(station: Station) -> Logged:
    return (
        (radio_boot() >> radio_tune(station))
        & led_fade("Play", 0.0, 1.0)
        & led_fade("Next station", 0.0, 1.0)
        & led_fade("Prev station", 0.0, 1.0)
    )


def ux_retune(station: Station) -> Logged:
    return (
        radio_tune(station)
        & led_pulse("Play", 1.0, 0.0)
        & led_pulse("Next station", 1.0, 0.0)
        & led_pulse("Prev station", 1.0, 0.0)
    )


def ux_next_station(station: Station) -> Logged:
    return radio_tune(station) & led_pulse("Play", 1.0, 0.0) & led_pulse("Next station", 1.0, 0.0)


def ux_prev_station(station: Station) -> Logged:
    return radio_tune(station) & led_pulse("Play", 1.0, 0.0) & led_pulse("Prev station", 1.0, 0.0)


def ux_pause() -> Logged:
    return (
        radio_pause()
        & led_fade("Play", 1.0, 0.0)
        & led_fade("Next station", 1.0, 0.0)
        & led_fade("Prev station", 1.0, 0.0)
    )

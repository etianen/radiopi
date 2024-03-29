from __future__ import annotations

import logging
from argparse import ArgumentParser
from collections.abc import Generator
from contextlib import contextmanager
from signal import pause

from radiopi.buttons import create_buttons
from radiopi.led_controller import LED_CONTROLLERS, LEDControllerName
from radiopi.leds import create_leds, leds_watcher
from radiopi.log import log_contextmanager
from radiopi.pin_factory import PIN_FACTORIES, PinFactoryName, create_pin_factory
from radiopi.radio import Radio, State, radio_watcher
from radiopi.runner import RUNNERS, RunnerName, create_runner
from radiopi.station import load_stations


@log_contextmanager(name="Main")
@contextmanager
def running(
    *,
    duration: float,
    led_controller_name: LEDControllerName,
    pin_factory_name: PinFactoryName,
    runner_name: RunnerName,
) -> Generator[Radio, None, None]:
    stations = load_stations()
    state = State(
        playing=False,
        station_index=0,
        stations=stations,
        stopping=False,
    )
    led_controller_cls = LED_CONTROLLERS[led_controller_name]
    radio = Radio(state)
    runner = create_runner(runner_name)
    # Start contexts.
    with (
        create_pin_factory(pin_factory_name) as pin_factory,
        create_buttons(pin_factory=pin_factory, radio=radio, runner=runner),
        create_leds(led_controller_cls=led_controller_cls, pin_factory=pin_factory) as leds,
        radio_watcher(radio, runner=runner),
        leds_watcher(radio, led_controller_cls=led_controller_cls, leds=leds),
    ):
        radio.play()
        try:
            yield radio
        finally:
            radio.stop()


def main() -> None:  # pragma: no cover
    # Parse args.
    parser = ArgumentParser()
    parser.add_argument("--led-controller", choices=LED_CONTROLLERS, default="pwm")
    parser.add_argument("--pin-factory", choices=PIN_FACTORIES, default="rpigpio")
    parser.add_argument("--runner", choices=RUNNERS, default="subprocess")
    args = parser.parse_args()
    # Run radio.
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    with running(
        duration=0.3,
        led_controller_name=args.led_controller,
        pin_factory_name=args.pin_factory,
        runner_name=args.runner,
    ):
        try:
            pause()
        except KeyboardInterrupt:
            pass

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from queue import SimpleQueue

from radiopi import running as running_
from radiopi.leds import MockLEDController
from radiopi.radio import Radio, radio_boot_args, radio_tune_args
from radiopi.runner import Args, Runner


class QueueRunner(Runner):
    def __init__(self) -> None:
        self.queue: SimpleQueue[Args] = SimpleQueue()

    def _call(self, args: Args) -> None:
        self.queue.put_nowait(args)

    def assert_called(self, expected_args: Args) -> None:
        args = self.queue.get(timeout=1.0)
        assert args == expected_args


@contextmanager
def running(*, runner: QueueRunner) -> Generator[Radio, None, None]:
    with running_(duration=0.0, led_controller_cls=MockLEDController, pin_factory_name="mock", runner=runner) as radio:
        # On start, the radio automatically boots and tunes.
        runner.assert_called(radio_boot_args())
        runner.assert_called(radio_tune_args(radio.state.stations[0]))
        # All done!
        yield radio

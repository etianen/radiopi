from __future__ import annotations

from radiopi import running
from tests import QueueRunner


def test_starts_and_stops(runner: QueueRunner) -> None:
    with running(pin_factory_name="mock", runner=runner) as radio:
        pass

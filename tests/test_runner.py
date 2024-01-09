from __future__ import annotations

import pytest

from radiopi.runner import RUNNERS, RunnerName, create_runner


@pytest.mark.parametrize("runner_name", RUNNERS)
def test_create_runner(runner_name: RunnerName) -> None:
    runner = create_runner(runner_name)
    runner("true")

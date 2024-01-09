from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from shutil import which
from subprocess import check_call

Run = Callable[[Sequence[str]], None]

logger = logging.getLogger(__name__)


def discover_run() -> Run:
    logger.info("Run: Discovering")
    # Try to use the real run implementation.
    if which("radio_cli") is None:
        # Fall back to a mock run implementation.
        logger.warning("Run: `radio_cli` not available, using mock run!")
        run_impl = run_mock
    else:
        # Use the real run implementation.
        run_impl = run_subprocess
    # All done!
    logger.info("Run: Discovered: %s", run_impl.__name__)
    return run_impl


def run_subprocess(cmd: Sequence[str]) -> None:
    logger.info("Run: Subprocess: %s", " ".join(cmd))
    check_call(cmd)


def run_mock(cmd: Sequence[str]) -> None:
    logger.info("Run: Mock: %s", " ".join(cmd))

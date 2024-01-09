from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from subprocess import check_call

Run = Callable[[Sequence[str]], None]

logger = logging.getLogger(__name__)


def run(cmd: Sequence[str]) -> None:
    logger.info("Run: %s", " ".join(cmd))
    check_call(cmd)

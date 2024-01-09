from __future__ import annotations

import logging
from collections.abc import Callable
from subprocess import check_call

Run = Callable[[tuple[str, ...]], None]

logger = logging.getLogger(__name__)


def run(cmd: tuple[str, ...]) -> None:
    logger.info("Running `%s`", " ".join(cmd))
    check_call(cmd)

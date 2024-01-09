from __future__ import annotations

import logging
from collections.abc import Callable, Generator
from contextlib import AbstractContextManager, contextmanager
from functools import wraps
from threading import Thread
from typing import Any, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")

logger = logging.getLogger(__name__)


def daemon(*, name: str) -> Callable[[Callable[P, None]], Callable[P, AbstractContextManager[None]]]:
    def decorator(fn: Callable[P, None]) -> Callable[P, AbstractContextManager[None]]:
        @contextmanager
        @wraps(fn)
        def daemon_wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[None, None, None]:
            yield

        return daemon_wrapper

    return decorator

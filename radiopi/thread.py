from __future__ import annotations

import logging
from collections.abc import Callable, Generator
from contextlib import AbstractContextManager, contextmanager
from functools import wraps
from threading import Thread
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from radiopi.log import log_contextmanager

P = ParamSpec("P")
T = TypeVar("T")


def daemon(*, name: str) -> Callable[[Callable[P, None]], Callable[P, AbstractContextManager[None]]]:
    def decorator(fn: Callable[P, None]) -> Callable[P, AbstractContextManager[None]]:
        @wraps(fn)
        @log_contextmanager(name=name)
        @contextmanager
        def daemon_wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[None, None, None]:
            thread = Thread(daemon=True, name=name, target=fn, args=args, kwargs=kwargs)
            thread.start()
            try:
                yield
            finally:
                thread.join(timeout=15.0)
                if thread.is_alive():  # pragma: no cover
                    raise RuntimeError(f"{name}: Zombie")

        return daemon_wrapper

    return decorator

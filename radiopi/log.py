from __future__ import annotations

import logging
from collections.abc import Callable, Generator
from contextlib import AbstractContextManager, contextmanager
from functools import wraps
from typing import TypeVar

from typing_extensions import ParamSpec, TypeAlias

P = ParamSpec("P")
T = TypeVar("T")

ContextManagerCallable: TypeAlias = Callable[P, AbstractContextManager[T]]

logger = logging.getLogger(__name__)


def log_contextmanager(*, name: str) -> Callable[[ContextManagerCallable[P, T]], ContextManagerCallable[P, T]]:
    def decorator(fn: ContextManagerCallable[P, T]) -> ContextManagerCallable[P, T]:
        @wraps(fn)
        @contextmanager
        def log_contextmanager_wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[T, None, None]:
            logger.info("%s: Starting", name)
            with fn(*args, **kwargs) as ctx:
                logger.info("%s: Started", name)
                yield ctx
                logger.info("%s: Stopping", name)
            logger.info("%s: Stopped", name)

        return log_contextmanager_wrapper

    return decorator

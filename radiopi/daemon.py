from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import AbstractContextManager, contextmanager
from functools import wraps
from threading import Thread

from typing_extensions import ParamSpec, TypeAlias

from radiopi.log import log_contextmanager

P = ParamSpec("P")

DaemonCallable: TypeAlias = Callable[P, None]
DaemonContextManagerCallable: TypeAlias = Callable[P, AbstractContextManager[None]]


def daemon(*, name: str) -> Callable[[DaemonCallable[P]], DaemonContextManagerCallable[P]]:
    def decorator(fn: DaemonCallable[P]) -> DaemonContextManagerCallable[P]:
        @wraps(fn)
        @log_contextmanager(name=name)
        @contextmanager
        def daemon_wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[None, None, None]:
            thread = Thread(name=name, daemon=True, target=fn, args=args, kwargs=kwargs)
            thread.start()
            try:
                yield
            finally:
                thread.join(timeout=15.0)
                if thread.is_alive():  # pragma: no cover
                    raise RuntimeError(f"{name}: Zombie")

        return daemon_wrapper

    return decorator

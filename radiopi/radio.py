from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class State:
    is_playing: bool
    station_index: int


class Radio:
    def __init__(self, *, )

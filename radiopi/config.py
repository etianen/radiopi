from __future__ import annotations

import dataclasses


@dataclasses.dataclass()
class Config:
    """
    Global RadioPi config.
    """

    radio_cli_path: str = "radio_cli"
    """
    Path of the DABBoard `radio_cli` binary.

    This is resolved relative to `$PATH`.
    """

    station_list_path: str = "/etc/radiopi/stations.json"
    """
    Path of the stations list JSON file.
    """

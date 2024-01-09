from __future__ import annotations

import dataclasses
import json
import logging
from collections.abc import Sequence
from pathlib import Path

logger = logging.getLogger()


@dataclasses.dataclass(frozen=True)
class Station:
    frequency_index: int
    service_id: int
    component_id: int
    label: str


def load_stations() -> Sequence[Station]:
    logger.info("Stations: Loading")
    # Load station data.
    data = json.loads((Path(__file__).parent.parent / "stations.json").read_bytes())
    # Build the station mapping.
    stations: list[Station] = []
    for ensemble_data in data["ensembleList"]:
        frequency_index = ensemble_data["EnsembleNo"]
        digital_service_list_data = ensemble_data.get("DigitalServiceList", {})
        service_list_data = digital_service_list_data.get("ServiceList", [])
        # Look at all services.
        for service_data in service_list_data:
            service_id = service_data["ServId"]
            label = service_data["Label"].strip()
            # Look at all components.
            for component_data in service_data["ComponentList"]:
                component_id = component_data["comp_ID"]
                # Create the station info.
                station = Station(
                    frequency_index=frequency_index,
                    service_id=service_id,
                    component_id=component_id,
                    label=label,
                )
                # Store the mapping.
                stations.append(station)
    # All done!
    logger.info("Stations: Loaded")
    return (*stations,)

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table


@dataclasses.dataclass()
class Station:
    frequency_index: int
    service_id: int
    component_id: int
    label: str


def load_stations() -> list[Station]:
    # Load station data.
    data = json.loads(Path("stations.json").read_bytes())
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
    return stations


def main() -> None:
    # Create the table.
    table = Table(title="Stations")
    table.add_column("Label", style="bold")
    table.add_column("Frequency index")
    table.add_column("Service ID")
    table.add_column("Component ID")
    # Add all stations.
    for station in load_stations():
        table.add_row(
            station.label,
            str(station.frequency_index),
            str(station.service_id),
            str(station.component_id),
        )
    # Print the table.
    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.models.emergency import IncidentType, UnitType


@dataclass(frozen=True)
class DecisionResult:
    recommended_unit_types: list[UnitType]
    operator_script: list[str]


class IncidentDecisionTree:
    def decide(self, *, incident_type: IncidentType) -> DecisionResult:
        if incident_type == "medical":
            return DecisionResult(
                recommended_unit_types=["ambulance", "police"],
                operator_script=[
                    "Confirm patient is conscious and breathing.",
                    "Ask for exact location and landmark.",
                    "Ask for number of affected people.",
                    "Provide basic first-aid instructions if safe.",
                ],
            )

        if incident_type == "fire":
            return DecisionResult(
                recommended_unit_types=["fire_truck", "ambulance", "police"],
                operator_script=[
                    "Confirm if there are people trapped.",
                    "Ask if the fire involves gas/chemicals.",
                    "Advise evacuation if safe.",
                    "Request caller to stay at a safe distance.",
                ],
            )

        if incident_type == "accident":
            return DecisionResult(
                recommended_unit_types=["ambulance", "police"],
                operator_script=[
                    "Confirm number of vehicles involved.",
                    "Ask if anyone is injured or unconscious.",
                    "Ask if the road is blocked.",
                    "Advise caller to turn on hazard lights if safe.",
                ],
            )

        raise ValueError("Unknown incident type")


DispatchPriority = Literal["High", "Medium", "Low"]


def priority_rank(priority: DispatchPriority) -> int:
    mapping = {"High": 0, "Medium": 1, "Low": 2}
    if priority not in mapping:
        raise ValueError("Unknown priority")
    return mapping[priority]


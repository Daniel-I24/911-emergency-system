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
                    "Confirma si el paciente está consciente y respirando.",
                    "Solicita la ubicación exacta y un punto de referencia.",
                    "Pregunta cuántas personas están afectadas.",
                    "Da instrucciones básicas de primeros auxilios si es seguro.",
                ],
            )

        if incident_type == "fire":
            return DecisionResult(
                recommended_unit_types=["fire_truck", "ambulance", "police"],
                operator_script=[
                    "Confirma si hay personas atrapadas.",
                    "Pregunta si el incendio involucra gas o químicos.",
                    "Recomienda evacuar si es seguro hacerlo.",
                    "Pide al llamante que se mantenga a una distancia segura.",
                ],
            )

        if incident_type == "accident":
            return DecisionResult(
                recommended_unit_types=["ambulance", "police"],
                operator_script=[
                    "Confirma cuántos vehículos están involucrados.",
                    "Pregunta si hay heridos o personas inconscientes.",
                    "Pregunta si la vía está bloqueada.",
                    "Indica encender las luces de emergencia si es seguro.",
                ],
            )

        raise ValueError("Unknown incident type")


DispatchPriority = Literal["High", "Medium", "Low"]


def priority_rank(priority: DispatchPriority) -> int:
    mapping = {"High": 0, "Medium": 1, "Low": 2}
    if priority not in mapping:
        raise ValueError("Unknown priority")
    return mapping[priority]


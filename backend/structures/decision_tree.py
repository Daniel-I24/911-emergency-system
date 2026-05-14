from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.models.emergency import IncidentType, UnitType


@dataclass(frozen=True)
class DecisionResult:
    """
    Representa el resultado de una decisión basada en el tipo de incidente.
    
    Attributes:
        recommended_unit_types (list[UnitType]): Lista de tipos de unidades recomendadas para el incidente.
        operator_script (list[str]): Guion paso a paso recomendado para que el operador guíe al llamante.
    """
    recommended_unit_types: list[UnitType]
    operator_script: list[str]


class IncidentDecisionTree:
    """
    Estructura lógica similar a un árbol de decisiones simple para determinar las 
    recomendaciones según el tipo de emergencia.
    """
    def decide(self, *, incident_type: IncidentType) -> DecisionResult:
        """
        Toma una decisión basada en el tipo de incidente de emergencia.
        
        Args:
            incident_type (IncidentType): El tipo de incidente reportado.
            
        Returns:
            DecisionResult: Un objeto que contiene las unidades recomendadas y el guion del operador.
            
        Raises:
            ValueError: Si el tipo de incidente es desconocido.
        """
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
    """
    Convierte un nivel de prioridad de despacho (Alto, Medio, Bajo) en un rango numérico
    utilizado para el ordenamiento en la cola de prioridad.
    
    Args:
        priority (DispatchPriority): El nivel de prioridad textual.
        
    Returns:
        int: Un valor numérico donde 0 es la mayor prioridad y 2 es la menor.
        
    Raises:
        ValueError: Si el nivel de prioridad no es válido.
    """
    mapping = {"High": 0, "Medium": 1, "Low": 2}
    if priority not in mapping:
        raise ValueError("Unknown priority")
    return mapping[priority]


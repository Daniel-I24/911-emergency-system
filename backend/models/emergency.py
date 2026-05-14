from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional


IncidentType = Literal["accident", "fire", "medical"]
Priority = Literal["High", "Medium", "Low"]
UnitType = Literal["ambulance", "fire_truck", "police"]


@dataclass(frozen=True)
class EmergencyCall:
    """
    Representa una llamada de emergencia registrada en el sistema.
    
    Attributes:
        call_id (int): Identificador único de la llamada.
        incident_type (IncidentType): El tipo de incidente (ej. accidente, incendio, médico).
        priority (Priority): Nivel de prioridad (Alta, Media, Baja).
        location (str): Ubicación del incidente.
        description (str): Descripción de la emergencia proporcionada por el usuario.
        created_at (str): Fecha y hora en que se creó la llamada.
        status (Literal["pending", "dispatched"]): Estado actual de la llamada.
    """
    call_id: int
    incident_type: IncidentType
    priority: Priority
    location: str
    description: str
    created_at: str
    status: Literal["pending", "dispatched"]

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte la llamada de emergencia a un diccionario para facilitar su serialización (ej. JSON).
        """
        return {
            "call_id": self.call_id,
            "incident_type": self.incident_type,
            "priority": self.priority,
            "location": self.location,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status,
        }


@dataclass
class ResponseUnit:
    """
    Representa una unidad de respuesta disponible o asignable a las emergencias (ej. ambulancia).
    
    Attributes:
        unit_id (str): Identificador único de la unidad.
        unit_type (UnitType): El tipo de unidad de respuesta.
        location (str): Ubicación actual de la unidad.
        available (bool): Indica si la unidad está disponible para ser despachada.
    """
    unit_id: str
    unit_type: UnitType
    location: str
    available: bool = True

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte la unidad de respuesta a un diccionario.
        """
        return {
            "unit_id": self.unit_id,
            "unit_type": self.unit_type,
            "location": self.location,
            "available": self.available,
        }


@dataclass(frozen=True)
class DispatchRecord:
    """
    Registra el historial de un despacho, vinculando una llamada con la unidad que respondió.
    
    Attributes:
        dispatch_id (int): Identificador único del despacho.
        call_id (int): ID de la llamada de emergencia que se está atendiendo.
        unit_id (str): ID de la unidad enviada a la ubicación.
        unit_type (UnitType): El tipo de unidad que fue enviada.
        distance (int): Distancia calculada entre la unidad y la ubicación de la emergencia.
        dispatched_at (str): Fecha y hora del despacho.
        note (Optional[str]): Notas adicionales sobre el despacho.
    """
    dispatch_id: int
    call_id: int
    unit_id: str
    unit_type: UnitType
    distance: int
    dispatched_at: str
    note: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte el registro de despacho a un diccionario.
        """
        data = {
            "dispatch_id": self.dispatch_id,
            "call_id": self.call_id,
            "unit_id": self.unit_id,
            "unit_type": self.unit_type,
            "distance": self.distance,
            "dispatched_at": self.dispatched_at,
        }
        if self.note is not None:
            data["note"] = self.note
        return data


from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional


IncidentType = Literal["accident", "fire", "medical"]
Priority = Literal["High", "Medium", "Low"]
UnitType = Literal["ambulance", "fire_truck", "police"]


@dataclass(frozen=True)
class EmergencyCall:
    call_id: int
    incident_type: IncidentType
    priority: Priority
    location: str
    description: str
    created_at: str
    status: Literal["pending", "dispatched"]

    def to_dict(self) -> dict[str, Any]:
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
    unit_id: str
    unit_type: UnitType
    location: str
    available: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "unit_type": self.unit_type,
            "location": self.location,
            "available": self.available,
        }


@dataclass(frozen=True)
class DispatchRecord:
    dispatch_id: int
    call_id: int
    unit_id: str
    unit_type: UnitType
    distance: int
    dispatched_at: str
    note: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
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


from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.patient_service import PatientServiceError, patient_service


ROUTE_PATIENTS = "/patients"
ROUTE_PATIENTS_PREPEND = "/patients/prepend"
ROUTE_PATIENTS_INSERT = "/patients/insert/{index}"
ROUTE_PATIENTS_INDEX = "/patients/{index}"
ROUTE_PATIENTS_COUNT = "/patients/count"

MESSAGE_UNEXPECTED_ERROR = "Ocurrió un error inesperado."


class PatientPayload(BaseModel):
    """Represents the required patient payload for write operations."""

    id: int = Field(..., description="Unique patient ID")
    name: str = Field(..., min_length=1, description="Patient name")
    age: int = Field(..., ge=1, description="Patient age")
    priority: str = Field(..., description="Priority: Alta | Media | Baja")
    arrival_time: str = Field(..., min_length=1, description="Arrival time string")


def _response(*, success: bool, data: Any, message: str) -> dict[str, Any]:
    """Create a consistent JSON response structure."""
    return {"success": success, "data": data, "message": message}


router = APIRouter()


@router.get(ROUTE_PATIENTS)
def get_patients() -> dict[str, Any]:
    """Get all patients."""
    try:
        result = patient_service.get_all_patients()
        return _response(success=result.success, data=result.data, message=result.message)
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)


@router.post(ROUTE_PATIENTS)
def add_patient(payload: PatientPayload) -> dict[str, Any]:
    """Add a patient to the end of the queue."""
    try:
        result = patient_service.add_to_end(patient=payload.model_dump())
        return _response(success=result.success, data=result.data, message=result.message)
    except PatientServiceError as exc:
        return _response(success=False, data=None, message=str(exc))
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)


@router.post(ROUTE_PATIENTS_PREPEND)
def add_patient_to_start(payload: PatientPayload) -> dict[str, Any]:
    """Add a patient to the start of the queue."""
    try:
        result = patient_service.add_to_start(patient=payload.model_dump())
        return _response(success=result.success, data=result.data, message=result.message)
    except PatientServiceError as exc:
        return _response(success=False, data=None, message=str(exc))
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)


@router.post(ROUTE_PATIENTS_INSERT)
def insert_patient(index: int, payload: PatientPayload) -> dict[str, Any]:
    """Insert a patient at a specific position."""
    try:
        result = patient_service.insert_at_index(index=index, patient=payload.model_dump())
        return _response(success=result.success, data=result.data, message=result.message)
    except PatientServiceError as exc:
        return _response(success=False, data=None, message=str(exc))
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)


@router.delete(ROUTE_PATIENTS_INDEX)
def remove_patient(index: int) -> dict[str, Any]:
    """Remove a patient by position."""
    try:
        result = patient_service.remove_at_index(index=index)
        return _response(success=result.success, data=result.data, message=result.message)
    except PatientServiceError as exc:
        return _response(success=False, data=None, message=str(exc))
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)


@router.get(ROUTE_PATIENTS_COUNT)
def get_patient_count() -> dict[str, Any]:
    """Get the total number of patients."""
    try:
        result = patient_service.get_count()
        return _response(success=result.success, data=result.data, message=result.message)
    except Exception:
        return _response(success=False, data=None, message=MESSAGE_UNEXPECTED_ERROR)

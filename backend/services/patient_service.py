from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.structures.doubly_linked_list import DoublyLinkedList


KEY_ID = "id"
KEY_NAME = "name"
KEY_AGE = "age"
KEY_PRIORITY = "priority"
KEY_ARRIVAL_TIME = "arrival_time"

PRIORITY_HIGH = "Alta"
PRIORITY_MEDIUM = "Media"
PRIORITY_LOW = "Baja"
ALLOWED_PRIORITIES: tuple[str, ...] = (PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW)

MESSAGE_OK = "Operación exitosa."
MESSAGE_CREATED_END = "Paciente agregado al final."
MESSAGE_CREATED_START = "Paciente agregado al inicio."
MESSAGE_CREATED_AT_INDEX = "Paciente insertado en la posición indicada."
MESSAGE_REMOVED = "Paciente eliminado."
MESSAGE_EMPTY_LIST = "La lista está vacía."
MESSAGE_INVALID_INDEX = "Índice inválido."
MESSAGE_INVALID_FIELDS = "Datos del paciente incompletos o inválidos."
MESSAGE_DUPLICATE_ID = "Ya existe un paciente con ese ID."

MIN_AGE = 0
INDEX_MIN = 0


class PatientServiceError(ValueError):
    """Represents a controlled service-layer validation error."""

    pass


@dataclass(frozen=True)
class ServiceResult:
    """Standardized service return structure to be mapped into API responses."""

    success: bool
    data: Any
    message: str


class PatientService:
    """
    Encapsulates business logic for managing the patient queue.

    A single DoublyLinkedList instance is used as an in-memory store for the application.
    """

    def __init__(self, queue: DoublyLinkedList) -> None:
        """Create the service with a given DoublyLinkedList queue."""
        self._queue = queue

    def get_all_patients(self) -> ServiceResult:
        """Return all patients currently in the queue."""
        return ServiceResult(success=True, data=self._queue.get_all(), message=MESSAGE_OK)

    def get_count(self) -> ServiceResult:
        """Return the total number of patients currently in the queue."""
        return ServiceResult(success=True, data={"count": self._queue.get_length()}, message=MESSAGE_OK)

    def add_to_end(self, patient: dict[str, Any]) -> ServiceResult:
        """Validate and append a patient to the end of the queue."""
        self._validate_patient(patient=patient)
        self._queue.append(data=patient)
        return ServiceResult(success=True, data=patient, message=MESSAGE_CREATED_END)

    def add_to_start(self, patient: dict[str, Any]) -> ServiceResult:
        """Validate and prepend a patient to the start of the queue."""
        self._validate_patient(patient=patient)
        self._queue.prepend(data=patient)
        return ServiceResult(success=True, data=patient, message=MESSAGE_CREATED_START)

    def insert_at_index(self, index: int, patient: dict[str, Any]) -> ServiceResult:
        """Validate and insert a patient at a specific index."""
        self._validate_patient(patient=patient)
        if index < INDEX_MIN or index > self._queue.get_length():
            raise PatientServiceError(MESSAGE_INVALID_INDEX)
        self._queue.insert(index=index, data=patient)
        return ServiceResult(success=True, data=patient, message=MESSAGE_CREATED_AT_INDEX)

    def remove_at_index(self, index: int) -> ServiceResult:
        """Remove a patient by index and return the removed patient data."""
        if self._queue.get_length() == 0:
            raise PatientServiceError(MESSAGE_EMPTY_LIST)
        if index < INDEX_MIN or index >= self._queue.get_length():
            raise PatientServiceError(MESSAGE_INVALID_INDEX)
        removed = self._queue.remove(index=index)
        return ServiceResult(success=True, data=removed, message=MESSAGE_REMOVED)

    def _validate_patient(self, patient: dict[str, Any]) -> None:
        """Validate patient payload fields and enforce basic constraints."""
        if not isinstance(patient, dict):
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)

        required_keys = (KEY_ID, KEY_NAME, KEY_AGE, KEY_PRIORITY, KEY_ARRIVAL_TIME)
        for key in required_keys:
            if key not in patient:
                raise PatientServiceError(MESSAGE_INVALID_FIELDS)

        patient_id = patient.get(KEY_ID)
        name = patient.get(KEY_NAME)
        age = patient.get(KEY_AGE)
        priority = patient.get(KEY_PRIORITY)
        arrival_time = patient.get(KEY_ARRIVAL_TIME)

        if not isinstance(patient_id, int):
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)
        if self._queue.find_by_id(patient_id=patient_id) is not None:
            raise PatientServiceError(MESSAGE_DUPLICATE_ID)

        if not isinstance(name, str) or not name.strip():
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)
        if not isinstance(age, int) or age <= MIN_AGE:
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)
        if priority not in ALLOWED_PRIORITIES:
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)
        if not isinstance(arrival_time, str) or not arrival_time.strip():
            raise PatientServiceError(MESSAGE_INVALID_FIELDS)


global_queue = DoublyLinkedList()
patient_service = PatientService(queue=global_queue)

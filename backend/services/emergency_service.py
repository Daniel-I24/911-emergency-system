from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from time import time
from typing import Any, Literal, Optional

from backend.models.emergency import EmergencyCall, IncidentType, Priority, ResponseUnit, UnitType
from backend.structures.circular_array import CircularArray
from backend.structures.decision_tree import IncidentDecisionTree, priority_rank
from backend.structures.graph import WeightedGraph
from backend.structures.priority_queue import PriorityQueue
from backend.structures.queue import Queue
from backend.structures.singly_linked_list import SinglyLinkedList
from backend.structures.stack import Stack


class EmergencyServiceError(ValueError):
    pass


@dataclass(frozen=True)
class ServiceResult:
    """
    Representa el resultado estándar de una operación del servicio.
    
    Attributes:
        success (bool): Indica si la operación fue exitosa.
        data (Any): Los datos resultantes de la operación (si aplica).
        message (str): Mensaje descriptivo sobre el resultado o el error.
    """
    success: bool
    data: Any
    message: str


UndoKind = Literal["create_call", "dispatch", "cancel_call"]


@dataclass(frozen=True)
class UndoAction:
    """
    Representa una acción previa que puede ser deshecha por el sistema.
    
    Attributes:
        kind (UndoKind): El tipo de acción (crear llamada, despachar, cancelar).
        call_id (int): El ID de la llamada involucrada.
        unit_id (Optional[str]): El ID de la unidad involucrada (para despacho).
        unit_prev_location (Optional[str]): Ubicación previa de la unidad.
        unit_prev_available (Optional[bool]): Estado previo de disponibilidad de la unidad.
        call_snapshot (Optional[dict]): Copia de los datos de la llamada antes de ser modificada o eliminada.
    """
    kind: UndoKind
    call_id: int
    unit_id: Optional[str] = None
    unit_prev_location: Optional[str] = None
    unit_prev_available: Optional[bool] = None
    call_snapshot: Optional[dict[str, Any]] = None


class EmergencyService:
    """
    Servicio principal que gestiona la lógica de negocio del sistema de emergencias 911.
    Coordina llamadas, unidades, rutas, prioridades y el historial de acciones.
    """
    def __init__(self) -> None:
        self._calls: dict[int, dict[str, Any]] = {}
        self._pending: PriorityQueue = PriorityQueue()
        self._history: SinglyLinkedList = SinglyLinkedList()
        self._events: Queue[str] = Queue()
        self._undo: Stack[UndoAction] = Stack()
        self._decision_tree: IncidentDecisionTree = IncidentDecisionTree()
        self._graph: WeightedGraph = WeightedGraph()

        self._units: list[dict[str, Any]] = []
        self._unit_by_id: dict[str, dict[str, Any]] = {}
        self._rosters: dict[UnitType, CircularArray[str]] = {
            "ambulance": CircularArray(),
            "fire_truck": CircularArray(),
            "police": CircularArray(),
        }

        self._seed_demo_city()

    def list_locations(self) -> ServiceResult:
        """Devuelve todas las ubicaciones registradas en el mapa (grafo)."""
        return ServiceResult(success=True, data={"locations": self._graph.nodes()}, message="OK")

    def list_units(self) -> ServiceResult:
        """Devuelve la lista de todas las unidades de respuesta y su estado."""
        return ServiceResult(success=True, data=list(self._units), message="OK")

    def list_pending_calls(self) -> ServiceResult:
        """Devuelve una lista de las llamadas pendientes ordenadas por prioridad y secuencia."""
        call_ids = self._pending.to_list()
        calls = [self._calls[cid] for cid in call_ids if cid in self._calls]
        return ServiceResult(success=True, data=calls, message="OK")

    def list_all_calls(self) -> ServiceResult:
        return ServiceResult(success=True, data=list(self._calls.values()), message="OK")

    def get_history(self) -> ServiceResult:
        return ServiceResult(success=True, data=self._history.get_all(), message="OK")

    def get_events(self) -> ServiceResult:
        return ServiceResult(success=True, data={"events": self._events.to_list()}, message="OK")

    def pop_event(self) -> ServiceResult:
        if self._events.is_empty():
            raise EmergencyServiceError("No events")
        return ServiceResult(success=True, data={"event": self._events.dequeue()}, message="OK")

    def clear_events(self) -> ServiceResult:
        cleared: list[str] = []
        while not self._events.is_empty():
            cleared.append(self._events.dequeue())
        return ServiceResult(success=True, data={"count": len(cleared)}, message="OK")

    def get_distance(self, *, source: str, target: str) -> ServiceResult:
        """
        Calcula la distancia más corta entre dos ubicaciones utilizando el algoritmo de Dijkstra.
        """
        if source not in self._graph.nodes() or target not in self._graph.nodes():
            raise EmergencyServiceError("Unknown location")
        distances = self._graph.dijkstra_distances(source=source)
        if target not in distances or distances[target] >= 10**12:
            return ServiceResult(success=False, data={"source": source, "target": target}, message="No route")
        return ServiceResult(success=True, data={"source": source, "target": target, "distance": int(distances[target])}, message="OK")

    def get_operator_guide(self, *, incident_type: IncidentType) -> ServiceResult:
        decision = self._decision_tree.decide(incident_type=incident_type)
        return ServiceResult(
            success=True,
            data={
                "incident_type": incident_type,
                "recommended_unit_types": decision.recommended_unit_types,
                "operator_script": decision.operator_script,
            },
            message="OK",
        )

    def create_call(
        self,
        *,
        incident_type: IncidentType,
        priority: Priority,
        location: str,
        description: str,
    ) -> ServiceResult:
        """
        Registra una nueva llamada de emergencia en el sistema, agregándola a la cola de pendientes.
        """
        if location not in self._graph.nodes():
            raise EmergencyServiceError("Unknown location")
        if not description.strip():
            raise EmergencyServiceError("Description is required")

        call_id = int(time() * 1000)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        call = EmergencyCall(
            call_id=call_id,
            incident_type=incident_type,
            priority=priority,
            location=location,
            description=description.strip(),
            created_at=created_at,
            status="pending",
        ).to_dict()

        self._calls[call_id] = call
        self._pending.enqueue(call_id=call_id, rank=priority_rank(priority))
        self._events.enqueue(f"call_created:{call_id}")
        self._undo.push(UndoAction(kind="create_call", call_id=call_id))

        return ServiceResult(success=True, data=call, message="Call created")

    def cancel_call(self, *, call_id: int) -> ServiceResult:
        call = self._calls.get(call_id)
        if call is None:
            raise EmergencyServiceError("Call not found")
        if call.get("status") != "pending":
            raise EmergencyServiceError("Only pending calls can be canceled")

        self._pending.remove(call_id=call_id)
        removed = self._calls.pop(call_id)
        self._events.enqueue(f"call_canceled:{call_id}")
        self._undo.push(UndoAction(kind="cancel_call", call_id=call_id, call_snapshot=removed))
        return ServiceResult(success=True, data=removed, message="Call canceled")

    def add_unit(self, *, unit_id: str, unit_type: UnitType, location: str, available: bool) -> ServiceResult:
        unit_id = unit_id.strip()
        if not unit_id:
            raise EmergencyServiceError("Unit ID is required")
        if unit_id in self._unit_by_id:
            raise EmergencyServiceError("Unit ID already exists")
        if location not in self._graph.nodes():
            raise EmergencyServiceError("Unknown location")

        unit = ResponseUnit(unit_id=unit_id, unit_type=unit_type, location=location, available=available).to_dict()
        self._units.append(unit)
        self._unit_by_id[unit_id] = unit
        self._rebuild_rosters()
        self._events.enqueue(f"unit_added:{unit_id}")
        return ServiceResult(success=True, data=unit, message="Unit added")

    def update_unit(self, *, unit_id: str, location: Optional[str], available: Optional[bool]) -> ServiceResult:
        if unit_id not in self._unit_by_id:
            raise EmergencyServiceError("Unknown unit")
        unit = self._unit_by_id[unit_id]

        if location is not None:
            if location not in self._graph.nodes():
                raise EmergencyServiceError("Unknown location")
            unit["location"] = location

        if available is not None:
            unit["available"] = bool(available)

        self._rebuild_rosters()
        self._events.enqueue(f"unit_updated:{unit_id}")
        return ServiceResult(success=True, data=unit, message="Unit updated")

    def dispatch_next(self) -> ServiceResult:
        """
        Asigna la unidad de respuesta más adecuada a la llamada de emergencia con mayor prioridad.
        Calcula la ruta más corta y utiliza un sistema de rotación en caso de empate.
        """
        if self._pending.is_empty():
            raise EmergencyServiceError("No pending calls")

        call_id = self._pending.peek_next()
        call = self._calls.get(call_id)
        if call is None:
            self._pending.pop_next()
            raise EmergencyServiceError("Call not found")

        decision = self._decision_tree.decide(incident_type=call["incident_type"])
        candidates = self._available_units(unit_types=decision.recommended_unit_types)
        if not candidates:
            return ServiceResult(success=False, data={"call": call, "recommended_unit_types": decision.recommended_unit_types}, message="No available units")

        distances = self._graph.dijkstra_distances(source=call["location"])
        best_distance = None
        best_units: list[dict[str, Any]] = []
        for unit in candidates:
            unit_location = unit.get("location")
            if unit_location not in distances:
                continue
            dist = int(distances[unit_location])
            if best_distance is None or dist < best_distance:
                best_distance = dist
                best_units = [unit]
            elif dist == best_distance:
                best_units.append(unit)

        if best_distance is None or not best_units:
            return ServiceResult(success=False, data={"call": call}, message="No route found")

        chosen = self._pick_by_rotation(best_units)
        if chosen is None:
            chosen = best_units[0]

        self._pending.pop_next()

        unit_id = str(chosen["unit_id"])
        unit_prev_location = str(chosen.get("location"))
        unit_prev_available = bool(chosen.get("available"))

        chosen["available"] = False
        chosen["location"] = call["location"]
        call["status"] = "dispatched"

        dispatch_id = int(time() * 1000)
        dispatched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "dispatch_id": dispatch_id,
            "call_id": call_id,
            "unit_id": unit_id,
            "unit_type": chosen["unit_type"],
            "distance": int(best_distance),
            "dispatched_at": dispatched_at,
            "incident_type": call["incident_type"],
            "priority": call["priority"],
            "location": call["location"],
        }
        self._history.append(data=record)
        self._events.enqueue(f"dispatched:{call_id}:{unit_id}")
        self._undo.push(
            UndoAction(
                kind="dispatch",
                call_id=call_id,
                unit_id=unit_id,
                unit_prev_location=unit_prev_location,
                unit_prev_available=unit_prev_available,
            )
        )

        return ServiceResult(success=True, data={"call": call, "unit": chosen, "dispatch": record}, message="Dispatched")

    def undo_last(self) -> ServiceResult:
        """
        Deshace la última acción destructiva o que altera el estado general (creación de llamada, despacho o cancelación),
        utilizando la pila de acciones (Stack LIFO).
        """
        if self._undo.is_empty():
            raise EmergencyServiceError("Nothing to undo")

        action = self._undo.pop()
        if action.kind == "create_call":
            removed = self._calls.pop(action.call_id, None)
            self._pending.remove(call_id=action.call_id)
            self._events.enqueue(f"undo_create_call:{action.call_id}")
            return ServiceResult(success=True, data=removed, message="Undone")

        if action.kind == "dispatch":
            call = self._calls.get(action.call_id)
            if call is None:
                raise EmergencyServiceError("Call not found")

            if action.unit_id is None or action.unit_id not in self._unit_by_id:
                raise EmergencyServiceError("Unit not found")

            unit = self._unit_by_id[action.unit_id]
            if action.unit_prev_location is not None:
                unit["location"] = action.unit_prev_location
            if action.unit_prev_available is not None:
                unit["available"] = action.unit_prev_available

            call["status"] = "pending"
            self._pending.enqueue(call_id=action.call_id, rank=priority_rank(call["priority"]))
            self._rebuild_rosters()

            undo_record = {
                "dispatch_id": int(time() * 1000),
                "call_id": action.call_id,
                "unit_id": action.unit_id,
                "unit_type": unit.get("unit_type"),
                "distance": 0,
                "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "note": "undo",
            }
            self._history.append(data=undo_record)
            self._events.enqueue(f"undo_dispatch:{action.call_id}:{action.unit_id}")
            return ServiceResult(success=True, data={"call": call, "unit": unit}, message="Undone")

        if action.kind == "cancel_call":
            if action.call_snapshot is None:
                raise EmergencyServiceError("Nothing to undo")
            self._calls[action.call_id] = action.call_snapshot
            self._pending.enqueue(call_id=action.call_id, rank=priority_rank(action.call_snapshot["priority"]))
            self._events.enqueue(f"undo_cancel_call:{action.call_id}")
            return ServiceResult(success=True, data=action.call_snapshot, message="Undone")

        raise EmergencyServiceError("Unsupported undo")

    def _available_units(self, *, unit_types: list[UnitType]) -> list[dict[str, Any]]:
        return [u for u in self._units if u.get("available") is True and u.get("unit_type") in unit_types]

    def _pick_by_rotation(self, candidates: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if not candidates:
            return None

        unit_type = candidates[0].get("unit_type")
        if unit_type not in self._rosters:
            return None

        roster = self._rosters[unit_type]
        candidate_ids = {str(u.get("unit_id")) for u in candidates}
        if roster.is_empty():
            return None

        attempts = len(roster.to_list())
        for _ in range(attempts):
            next_id = roster.next()
            if next_id in candidate_ids:
                return self._unit_by_id.get(next_id)
        return None

    def _rebuild_rosters(self) -> None:
        grouped: dict[UnitType, list[str]] = {"ambulance": [], "fire_truck": [], "police": []}
        for unit in self._units:
            unit_type = unit.get("unit_type")
            unit_id = unit.get("unit_id")
            if unit_type in grouped and unit_id is not None:
                grouped[unit_type].append(str(unit_id))

        for unit_type, ids in grouped.items():
            self._rosters[unit_type].set_items(ids)

    def _seed_demo_city(self) -> None:
        for node in ["Downtown", "North", "South", "East", "West", "Hospital", "Station1", "Station2"]:
            self._graph.add_node(node)

        self._graph.add_undirected_edge(a="Downtown", b="North", weight=4)
        self._graph.add_undirected_edge(a="Downtown", b="South", weight=5)
        self._graph.add_undirected_edge(a="Downtown", b="East", weight=3)
        self._graph.add_undirected_edge(a="Downtown", b="West", weight=6)
        self._graph.add_undirected_edge(a="Hospital", b="Downtown", weight=2)
        self._graph.add_undirected_edge(a="Station1", b="East", weight=2)
        self._graph.add_undirected_edge(a="Station1", b="North", weight=3)
        self._graph.add_undirected_edge(a="Station2", b="West", weight=2)
        self._graph.add_undirected_edge(a="Station2", b="South", weight=3)

        self.add_unit(unit_id="A1", unit_type="ambulance", location="Hospital", available=True)
        self.add_unit(unit_id="A2", unit_type="ambulance", location="North", available=True)
        self.add_unit(unit_id="F1", unit_type="fire_truck", location="Station1", available=True)
        self.add_unit(unit_id="P1", unit_type="police", location="Downtown", available=True)


emergency_service = EmergencyService()


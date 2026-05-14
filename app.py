from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.services.emergency_service import EmergencyServiceError, emergency_service


class Emergency911App:
    """
    Clase principal de la aplicación para la interfaz de usuario del Sistema de Emergencias 911.
    Proporciona una interfaz gráfica para interactuar con los servicios de emergencia del backend,
    gestionar llamadas, unidades, historial de despachos y cálculo de rutas.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa la ventana principal de la aplicación y sus variables.
        
        Args:
            root (tk.Tk): La ventana raíz de tkinter.
        """
        self.root = root
        self.root.title("911 Emergency System")
        self.root.geometry("1180x740")

        self.status_var = tk.StringVar(value="Ready")

        self.incident_var = tk.StringVar(value="medical")
        self.priority_var = tk.StringVar(value="Medium")
        self.location_var = tk.StringVar(value="")
        self.description_var = tk.StringVar(value="")

        self.distance_source_var = tk.StringVar(value="")
        self.distance_target_var = tk.StringVar(value="")

        self.unit_id_var = tk.StringVar(value="")
        self.unit_type_var = tk.StringVar(value="ambulance")
        self.unit_location_var = tk.StringVar(value="")
        self.unit_available_var = tk.BooleanVar(value=True)

        self._build_layout()
        self.refresh_all()

    def _build_layout(self) -> None:
        """
        Construye el diseño principal de la aplicación, incluyendo encabezados,
        marcos para la creación de llamadas de emergencia, llamadas pendientes, gestión de unidades,
        historial y cola de eventos.
        """
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(header, text="911 Emergency System", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w")

        actions = ttk.Frame(header)
        actions.grid(row=0, column=1, sticky="e")

        ttk.Button(actions, text="Refresh", command=self.refresh_all).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(actions, text="Dispatch Next", command=self.dispatch_next).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(actions, text="Undo Last", command=self.undo_last).grid(row=0, column=2)

        body = ttk.Frame(main)
        body.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)
        body.rowconfigure(2, weight=0)

        left_top = ttk.Labelframe(body, text="Create Emergency Call", padding=12)
        left_top.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        left_top.columnconfigure(1, weight=1)

        ttk.Label(left_top, text="Incident type").grid(row=0, column=0, sticky="w")
        self.incident_cb = ttk.Combobox(left_top, textvariable=self.incident_var, state="readonly")
        self.incident_cb["values"] = ("accident", "fire", "medical")
        self.incident_cb.grid(row=0, column=1, sticky="ew")
        ttk.Button(left_top, text="Guide", command=self.show_guide).grid(row=0, column=2, padx=(8, 0))

        ttk.Label(left_top, text="Priority").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.priority_cb = ttk.Combobox(left_top, textvariable=self.priority_var, state="readonly")
        self.priority_cb["values"] = ("High", "Medium", "Low")
        self.priority_cb.grid(row=1, column=1, sticky="ew", pady=(10, 0))

        ttk.Label(left_top, text="Location").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.location_cb = ttk.Combobox(left_top, textvariable=self.location_var, state="readonly")
        self.location_cb.grid(row=2, column=1, sticky="ew", pady=(10, 0))

        ttk.Label(left_top, text="Description").grid(row=3, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(left_top, textvariable=self.description_var).grid(row=3, column=1, sticky="ew", pady=(10, 0))

        ttk.Button(left_top, text="Create Call", command=self.create_call).grid(row=4, column=1, sticky="e", pady=(12, 0))

        right_top = ttk.Labelframe(body, text="Route Distance (Dijkstra)", padding=12)
        right_top.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
        right_top.columnconfigure(1, weight=1)

        ttk.Label(right_top, text="Source").grid(row=0, column=0, sticky="w")
        self.distance_source_cb = ttk.Combobox(right_top, textvariable=self.distance_source_var, state="readonly")
        self.distance_source_cb.grid(row=0, column=1, sticky="ew")

        ttk.Label(right_top, text="Target").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.distance_target_cb = ttk.Combobox(right_top, textvariable=self.distance_target_var, state="readonly")
        self.distance_target_cb.grid(row=1, column=1, sticky="ew", pady=(10, 0))

        ttk.Button(right_top, text="Compute", command=self.compute_distance).grid(row=2, column=1, sticky="e", pady=(12, 0))

        left_bottom = ttk.Labelframe(body, text="Pending Calls (Priority Order)", padding=12)
        left_bottom.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        left_bottom.rowconfigure(0, weight=1)
        left_bottom.columnconfigure(0, weight=1)

        call_actions = ttk.Frame(left_bottom)
        call_actions.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(call_actions, text="Cancel selected", command=self.cancel_selected_call).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(call_actions, text="Copy details", command=self.copy_selected_call).grid(row=0, column=1)

        self.calls_tree = ttk.Treeview(
            left_bottom,
            columns=("call_id", "type", "priority", "location", "created_at", "status"),
            show="headings",
        )
        for col, text, width in (
            ("call_id", "Call ID", 120),
            ("type", "Type", 90),
            ("priority", "Priority", 90),
            ("location", "Location", 120),
            ("created_at", "Created", 160),
            ("status", "Status", 90),
        ):
            self.calls_tree.heading(col, text=text)
            self.calls_tree.column(col, width=width, anchor="w")

        self.calls_tree.grid(row=0, column=0, sticky="nsew")
        calls_scroll = ttk.Scrollbar(left_bottom, orient="vertical", command=self.calls_tree.yview)
        calls_scroll.grid(row=0, column=1, sticky="ns")
        self.calls_tree.configure(yscrollcommand=calls_scroll.set)

        right_bottom = ttk.Labelframe(body, text="Units and Dispatch History", padding=12)
        right_bottom.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        right_bottom.rowconfigure(2, weight=1)
        right_bottom.columnconfigure(0, weight=1)

        units_frame = ttk.Frame(right_bottom)
        units_frame.grid(row=0, column=0, sticky="nsew")
        units_frame.columnconfigure(0, weight=1)

        self.units_tree = ttk.Treeview(units_frame, columns=("unit_id", "type", "location", "available"), show="headings", height=6)
        for col, text, width in (
            ("unit_id", "Unit", 80),
            ("type", "Type", 110),
            ("location", "Location", 120),
            ("available", "Available", 90),
        ):
            self.units_tree.heading(col, text=text)
            self.units_tree.column(col, width=width, anchor="w")
        self.units_tree.grid(row=0, column=0, sticky="nsew")
        units_scroll = ttk.Scrollbar(units_frame, orient="vertical", command=self.units_tree.yview)
        units_scroll.grid(row=0, column=1, sticky="ns")
        self.units_tree.configure(yscrollcommand=units_scroll.set)

        unit_form = ttk.Frame(right_bottom)
        unit_form.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        unit_form.columnconfigure(1, weight=1)
        unit_form.columnconfigure(3, weight=1)

        ttk.Label(unit_form, text="Unit ID").grid(row=0, column=0, sticky="w")
        ttk.Entry(unit_form, textvariable=self.unit_id_var, width=12).grid(row=0, column=1, sticky="ew", padx=(8, 12))

        ttk.Label(unit_form, text="Type").grid(row=0, column=2, sticky="w")
        unit_type_cb = ttk.Combobox(unit_form, textvariable=self.unit_type_var, state="readonly", width=14)
        unit_type_cb["values"] = ("ambulance", "fire_truck", "police")
        unit_type_cb.grid(row=0, column=3, sticky="ew", padx=(8, 0))

        ttk.Label(unit_form, text="Location").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.unit_location_cb = ttk.Combobox(unit_form, textvariable=self.unit_location_var, state="readonly")
        self.unit_location_cb.grid(row=1, column=1, sticky="ew", padx=(8, 12), pady=(10, 0))

        ttk.Checkbutton(unit_form, text="Available", variable=self.unit_available_var).grid(row=1, column=2, sticky="w", pady=(10, 0))
        ttk.Button(unit_form, text="Add unit", command=self.add_unit).grid(row=1, column=3, sticky="e", pady=(10, 0))

        unit_actions = ttk.Frame(unit_form)
        unit_actions.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        ttk.Button(unit_actions, text="Load selected", command=self.load_selected_unit).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(unit_actions, text="Update selected", command=self.update_selected_unit).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(unit_actions, text="Toggle availability", command=self.toggle_selected_unit).grid(row=0, column=2)

        history_frame = ttk.Frame(right_bottom)
        history_frame.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        history_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)

        self.history_tree = ttk.Treeview(
            history_frame,
            columns=("dispatch_id", "call_id", "unit_id", "unit_type", "distance", "time", "note"),
            show="headings",
        )
        for col, text, width in (
            ("dispatch_id", "Dispatch", 110),
            ("call_id", "Call", 110),
            ("unit_id", "Unit", 70),
            ("unit_type", "Type", 110),
            ("distance", "Distance", 80),
            ("time", "Time", 160),
            ("note", "Note", 80),
        ):
            self.history_tree.heading(col, text=text)
            self.history_tree.column(col, width=width, anchor="w")
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        history_scroll.grid(row=0, column=1, sticky="ns")
        self.history_tree.configure(yscrollcommand=history_scroll.set)

        events_frame = ttk.Labelframe(body, text="Event Queue", padding=12)
        events_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        events_frame.columnconfigure(0, weight=1)
        events_frame.rowconfigure(0, weight=1)

        self.events_list = tk.Listbox(events_frame, height=6)
        self.events_list.grid(row=0, column=0, sticky="nsew")
        events_scroll = ttk.Scrollbar(events_frame, orient="vertical", command=self.events_list.yview)
        events_scroll.grid(row=0, column=1, sticky="ns")
        self.events_list.configure(yscrollcommand=events_scroll.set)

        events_actions = ttk.Frame(events_frame)
        events_actions.grid(row=1, column=0, sticky="w", pady=(10, 0))
        ttk.Button(events_actions, text="Pop event", command=self.pop_event).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(events_actions, text="Clear events", command=self.clear_events).grid(row=0, column=1)

        footer = ttk.Frame(main)
        footer.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var).grid(row=0, column=0, sticky="w")

    def set_status(self, message: str) -> None:
        """
        Actualiza el mensaje de la barra de estado en la parte inferior de la ventana.
        
        Args:
            message (str): El mensaje de estado a mostrar.
        """
        self.status_var.set(message)

    def refresh_all(self) -> None:
        """
        Actualiza todos los componentes de la interfaz obteniendo los últimos datos del backend.
        Actualiza listas desplegables, árboles de unidades, llamadas, historial y eventos.
        """
        locations = emergency_service.list_locations().data["locations"]
        self.location_cb["values"] = tuple(locations)
        self.distance_source_cb["values"] = tuple(locations)
        self.distance_target_cb["values"] = tuple(locations)
        self.unit_location_cb["values"] = tuple(locations)

        if not self.location_var.get() and locations:
            self.location_var.set(locations[0])
        if not self.distance_source_var.get() and locations:
            self.distance_source_var.set(locations[0])
        if not self.distance_target_var.get() and len(locations) > 1:
            self.distance_target_var.set(locations[1])
        if not self.unit_location_var.get() and locations:
            self.unit_location_var.set(locations[0])

        self._render_units()
        self._render_calls()
        self._render_history()
        self._render_events()
        self.set_status("Refreshed")

    def _render_units(self) -> None:
        """
        Obtiene la lista actual de unidades desde el backend y actualiza la vista de árbol de unidades.
        """
        for item in self.units_tree.get_children():
            self.units_tree.delete(item)
        for unit in emergency_service.list_units().data:
            self.units_tree.insert(
                "",
                "end",
                values=(unit.get("unit_id"), unit.get("unit_type"), unit.get("location"), str(unit.get("available"))),
            )

    def _render_calls(self) -> None:
        """
        Obtiene la lista actual de llamadas de emergencia pendientes y actualiza la vista de árbol de llamadas.
        """
        for item in self.calls_tree.get_children():
            self.calls_tree.delete(item)
        for call in emergency_service.list_pending_calls().data:
            self.calls_tree.insert(
                "",
                "end",
                values=(
                    call.get("call_id"),
                    call.get("incident_type"),
                    call.get("priority"),
                    call.get("location"),
                    call.get("created_at"),
                    call.get("status"),
                ),
            )

    def _render_history(self) -> None:
        """
        Obtiene el historial de despachos y actualiza la vista de árbol del historial.
        Muestra hasta los últimos 200 registros.
        """
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        history = emergency_service.get_history().data
        for record in history[-200:]:
            self.history_tree.insert(
                "",
                "end",
                values=(
                    record.get("dispatch_id"),
                    record.get("call_id"),
                    record.get("unit_id"),
                    record.get("unit_type"),
                    record.get("distance"),
                    record.get("dispatched_at"),
                    record.get("note", ""),
                ),
            )

    def _render_events(self) -> None:
        """
        Obtiene los últimos eventos del sistema y actualiza la lista de eventos.
        Muestra hasta los últimos 200 eventos.
        """
        self.events_list.delete(0, "end")
        events = emergency_service.get_events().data["events"]
        for e in events[-200:]:
            self.events_list.insert("end", e)

    def _get_selected_call_id(self) -> int | None:
        """
        Recupera el ID de la llamada actualmente seleccionada en la vista de árbol de llamadas.
        
        Returns:
            int | None: El ID de la llamada seleccionada, o None si no hay ninguna llamada seleccionada.
        """
        selection = self.calls_tree.selection()
        if not selection:
            return None
        values = self.calls_tree.item(selection[0], "values")
        if not values:
            return None
        try:
            return int(values[0])
        except Exception:
            return None

    def cancel_selected_call(self) -> None:
        """
        Cancela la llamada de emergencia actualmente seleccionada en la interfaz de usuario.
        Muestra un mensaje de error si la operación falla.
        """
        call_id = self._get_selected_call_id()
        if call_id is None:
            self.set_status("Select a call first")
            return
        try:
            emergency_service.cancel_call(call_id=call_id)
            self.refresh_all()
            self.set_status(f"Canceled call {call_id}")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def copy_selected_call(self) -> None:
        """
        Copia los detalles de la llamada de emergencia actualmente seleccionada al portapapeles.
        """
        call_id = self._get_selected_call_id()
        if call_id is None:
            self.set_status("Select a call first")
            return
        for call in emergency_service.list_pending_calls().data:
            if call.get("call_id") == call_id:
                text = str(call)
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.set_status("Call copied to clipboard")
                return
        self.set_status("Call not found")

    def _get_selected_unit_id(self) -> str | None:
        """
        Recupera el ID de la unidad actualmente seleccionada en la vista de árbol de unidades.
        
        Returns:
            str | None: El ID de la unidad seleccionada, o None si no hay ninguna unidad seleccionada.
        """
        selection = self.units_tree.selection()
        if not selection:
            return None
        values = self.units_tree.item(selection[0], "values")
        if not values:
            return None
        return str(values[0])

    def load_selected_unit(self) -> None:
        """
        Carga los detalles de la unidad seleccionada desde la vista de árbol de unidades
        en el formulario de gestión de unidades para su edición.
        """
        unit_id = self._get_selected_unit_id()
        if unit_id is None:
            self.set_status("Select a unit first")
            return

        for unit in emergency_service.list_units().data:
            if str(unit.get("unit_id")) == unit_id:
                self.unit_id_var.set(unit_id)
                self.unit_type_var.set(str(unit.get("unit_type")))
                self.unit_location_var.set(str(unit.get("location")))
                self.unit_available_var.set(bool(unit.get("available")))
                self.set_status("Loaded unit")
                return

        self.set_status("Unit not found")

    def add_unit(self) -> None:
        """
        Añade una nueva unidad de emergencia utilizando los detalles proporcionados en el formulario de gestión.
        Muestra un mensaje de error si la operación falla.
        """
        try:
            unit_id = self.unit_id_var.get().strip()
            result = emergency_service.add_unit(
                unit_id=unit_id,
                unit_type=self.unit_type_var.get(),
                location=self.unit_location_var.get(),
                available=self.unit_available_var.get(),
            )
            self.refresh_all()
            self.unit_id_var.set("")
            self.set_status(f"Added unit {result.data['unit_id']}")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def update_selected_unit(self) -> None:
        """
        Actualiza la unidad seleccionada actualmente con la nueva ubicación y disponibilidad
        desde el formulario de gestión de unidades.
        """
        unit_id = self._get_selected_unit_id()
        if unit_id is None:
            self.set_status("Select a unit first")
            return
        try:
            emergency_service.update_unit(
                unit_id=unit_id,
                location=self.unit_location_var.get(),
                available=self.unit_available_var.get(),
            )
            self.refresh_all()
            self.set_status(f"Updated unit {unit_id}")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def toggle_selected_unit(self) -> None:
        """
        Alterna el estado de disponibilidad (disponible/no disponible) de la unidad seleccionada.
        """
        unit_id = self._get_selected_unit_id()
        if unit_id is None:
            self.set_status("Select a unit first")
            return
        try:
            units = emergency_service.list_units().data
            for unit in units:
                if str(unit.get("unit_id")) == unit_id:
                    new_value = not bool(unit.get("available"))
                    emergency_service.update_unit(unit_id=unit_id, location=None, available=new_value)
                    self.refresh_all()
                    self.set_status(f"Unit {unit_id} available={new_value}")
                    return
            self.set_status("Unit not found")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def pop_event(self) -> None:
        """
        Saca el siguiente evento de la cola de eventos del backend y muestra un mensaje de estado.
        """
        try:
            result = emergency_service.pop_event()
            self.refresh_all()
            self.set_status(f"Popped: {result.data['event']}")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def clear_events(self) -> None:
        """
        Limpia todos los eventos de la cola de eventos del backend.
        """
        try:
            result = emergency_service.clear_events()
            self.refresh_all()
            self.set_status(f"Cleared {result.data['count']} events")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def create_call(self) -> None:
        """
        Crea una nueva llamada de emergencia utilizando los detalles proporcionados en el formulario 'Create Emergency Call'.
        """
        try:
            result = emergency_service.create_call(
                incident_type=self.incident_var.get(),
                priority=self.priority_var.get(),
                location=self.location_var.get(),
                description=self.description_var.get(),
            )
            self.description_var.set("")
            self.refresh_all()
            self.set_status(f"Created call {result.data['call_id']}")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def dispatch_next(self) -> None:
        """
        Despacha la siguiente llamada de emergencia de mayor prioridad a una unidad disponible.
        Muestra un mensaje de éxito o de error basado en la disponibilidad.
        """
        try:
            result = emergency_service.dispatch_next()
            self.refresh_all()
            if result.success:
                call_id = result.data["call"]["call_id"]
                unit_id = result.data["unit"]["unit_id"]
                self.set_status(f"Dispatched call {call_id} to unit {unit_id}")
            else:
                self.set_status(result.message)
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def undo_last(self) -> None:
        """
        Deshace la última acción de despacho, restaurando la llamada a pendiente y liberando la unidad.
        """
        try:
            emergency_service.undo_last()
            self.refresh_all()
            self.set_status("Undone")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def compute_distance(self) -> None:
        """
        Calcula y muestra la ruta más corta entre la ubicación de origen y destino 
        seleccionadas utilizando el algoritmo de Dijkstra desde el backend.
        """
        try:
            result = emergency_service.get_distance(
                source=self.distance_source_var.get(),
                target=self.distance_target_var.get(),
            )
            if result.success:
                self.set_status(f"Shortest distance: {result.data['distance']}")
            else:
                self.set_status(result.message)
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def show_guide(self) -> None:
        """
        Abre una nueva ventana que muestra una guía para el operador basada en el tipo de incidente seleccionado.
        Incluye un script para el operador y los tipos de unidades recomendadas.
        """
        try:
            result = emergency_service.get_operator_guide(incident_type=self.incident_var.get())
            script = result.data["operator_script"]
            units = result.data["recommended_unit_types"]

            win = tk.Toplevel(self.root)
            win.title("Operator Guide")
            win.geometry("520x380")

            ttk.Label(win, text=f"Incident: {self.incident_var.get()}", font=("Segoe UI", 12, "bold")).pack(
                anchor="w", padx=12, pady=(12, 6)
            )
            ttk.Label(win, text=f"Recommended units: {', '.join(units)}").pack(anchor="w", padx=12)

            box = tk.Text(win, height=14, wrap="word")
            box.pack(fill="both", expand=True, padx=12, pady=12)
            for i, line in enumerate(script, start=1):
                box.insert("end", f"{i}. {line}\n")
            box.configure(state="disabled")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")


def main() -> None:
    """
    Punto de entrada principal de la aplicación. Inicializa la raíz de Tkinter,
    aplica los estilos y comienza el bucle de eventos principal.
    """
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except Exception:
        pass
    Emergency911App(root)
    root.mainloop()


if __name__ == "__main__":
    main()


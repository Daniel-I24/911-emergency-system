from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.services.emergency_service import EmergencyServiceError, emergency_service


class Emergency911App:
    def __init__(self, root: tk.Tk) -> None:
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

        self._build_layout()
        self.refresh_all()

    def _build_layout(self) -> None:
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
        right_bottom.rowconfigure(1, weight=1)
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

        history_frame = ttk.Frame(right_bottom)
        history_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
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

        footer = ttk.Frame(main)
        footer.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var).grid(row=0, column=0, sticky="w")

    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    def refresh_all(self) -> None:
        locations = emergency_service.list_locations().data["locations"]
        self.location_cb["values"] = tuple(locations)
        self.distance_source_cb["values"] = tuple(locations)
        self.distance_target_cb["values"] = tuple(locations)

        if not self.location_var.get() and locations:
            self.location_var.set(locations[0])
        if not self.distance_source_var.get() and locations:
            self.distance_source_var.set(locations[0])
        if not self.distance_target_var.get() and len(locations) > 1:
            self.distance_target_var.set(locations[1])

        self._render_units()
        self._render_calls()
        self._render_history()
        self.set_status("Refreshed")

    def _render_units(self) -> None:
        for item in self.units_tree.get_children():
            self.units_tree.delete(item)
        for unit in emergency_service.list_units().data:
            self.units_tree.insert(
                "",
                "end",
                values=(unit.get("unit_id"), unit.get("unit_type"), unit.get("location"), str(unit.get("available"))),
            )

    def _render_calls(self) -> None:
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

    def create_call(self) -> None:
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
        try:
            emergency_service.undo_last()
            self.refresh_all()
            self.set_status("Undone")
        except EmergencyServiceError as exc:
            self.set_status(str(exc))
        except Exception:
            self.set_status("An unexpected error occurred.")

    def compute_distance(self) -> None:
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
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except Exception:
        pass
    Emergency911App(root)
    root.mainloop()


if __name__ == "__main__":
    main()


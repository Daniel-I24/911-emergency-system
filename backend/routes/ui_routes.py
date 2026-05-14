from __future__ import annotations

from datetime import datetime
from html import escape
from time import time
from typing import Literal, Optional
from urllib.parse import quote

from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from backend.services.patient_service import PatientServiceError, patient_service


router = APIRouter()

UI_ROUTE = "/ui"
UI_ADD_END_ROUTE = "/ui/add-end"
UI_ADD_START_ROUTE = "/ui/add-start"
UI_INSERT_ROUTE = "/ui/insert"
UI_REMOVE_ROUTE = "/ui/remove/{index}"

PRIORITY_HIGH = "Alta"
PRIORITY_MEDIUM = "Media"
PRIORITY_LOW = "Baja"

MESSAGE_UNEXPECTED_ERROR = "Ocurrió un error inesperado."


@router.get("/", include_in_schema=False)
@router.get(UI_ROUTE, include_in_schema=False)
def ui(message: Optional[str] = None, kind: Optional[Literal["success", "error"]] = None) -> HTMLResponse:
    """Render the Spanish UI using server-side HTML generated in Python."""
    patients = patient_service.get_all_patients().data
    count = patient_service.get_count().data["count"]

    message_text = escape(message) if message else ""
    message_class = kind if kind in ("success", "error") else ""
    message_display = "block" if message_text else "none"

    rows_html = ""
    for index, patient in enumerate(patients):
        name = escape(str(patient.get("name", "")))
        age = escape(str(patient.get("age", "")))
        priority = escape(str(patient.get("priority", "")))
        arrival_time = escape(str(patient.get("arrival_time", "")))

        badge_class = "low"
        if patient.get("priority") == PRIORITY_HIGH:
            badge_class = "high"
        elif patient.get("priority") == PRIORITY_MEDIUM:
            badge_class = "medium"

        rows_html += (
            "<tr>"
            f"<td>{index}</td>"
            f"<td>{name}</td>"
            f"<td>{age}</td>"
            f"<td><span class='badge {badge_class}'>{priority}</span></td>"
            f"<td>{arrival_time}</td>"
            "<td>"
            f"<form method='post' action='/ui/remove/{index}' style='margin:0'>"
            "<button class='danger' type='submit'>Eliminar</button>"
            "</form>"
            "</td>"
            "</tr>"
        )

    if not rows_html:
        rows_html = "<tr><td class='muted' colspan='6'>No hay pacientes en la cola.</td></tr>"

    html = f"""
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Gestión de Pacientes — Sala de Emergencias</title>
    <style>
      :root {{
        --bg: #ffffff;
        --text: #111827;
        --muted: #6b7280;
        --border: #e5e7eb;
        --panel: #f9fafb;
        --danger: #dc2626;
        --warn: #f59e0b;
        --success: #16a34a;
        --primary: #2563eb;
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }}
      .container {{ max-width: 980px; margin: 0 auto; padding: 24px 16px 48px; }}
      header {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }}
      h1 {{ font-size: 20px; margin: 0; font-weight: 700; }}
      .stats {{ padding: 10px 12px; border: 1px solid var(--border); border-radius: 10px; background: var(--panel); color: var(--muted); font-size: 14px; white-space: nowrap; }}
      .grid {{ display: grid; grid-template-columns: 1fr; gap: 16px; margin: 16px 0 20px; }}
      @media (min-width: 840px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
      .card {{ border: 1px solid var(--border); border-radius: 12px; padding: 16px; background: #fff; }}
      .card h2 {{ margin: 0 0 10px; font-size: 16px; }}
      .form-row {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
      @media (min-width: 520px) {{
        .form-row.cols-3 {{ grid-template-columns: 1.5fr 0.8fr 1fr; }}
        .form-row.cols-2 {{ grid-template-columns: 1fr 1fr; }}
      }}
      label {{ display: block; font-size: 13px; color: var(--muted); margin-bottom: 6px; }}
      input, select {{ width: 100%; padding: 10px 10px; border: 1px solid var(--border); border-radius: 10px; font-size: 14px; outline: none; }}
      .actions {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }}
      button {{ border: 1px solid var(--border); background: #fff; padding: 10px 12px; border-radius: 10px; cursor: pointer; font-weight: 600; font-size: 14px; }}
      button.primary {{ border-color: rgba(37, 99, 235, 0.35); background: rgba(37, 99, 235, 0.08); color: var(--primary); }}
      button.danger {{ border-color: rgba(220, 38, 38, 0.35); background: rgba(220, 38, 38, 0.08); color: var(--danger); }}
      .message {{ margin-top: 12px; font-size: 14px; padding: 10px 12px; border-radius: 10px; border: 1px solid var(--border); background: var(--panel); color: var(--muted); display: {message_display}; }}
      .message.success {{ border-color: rgba(22, 163, 74, 0.35); background: rgba(22, 163, 74, 0.08); color: var(--success); }}
      .message.error {{ border-color: rgba(220, 38, 38, 0.35); background: rgba(220, 38, 38, 0.08); color: var(--danger); }}
      table {{ width: 100%; border-collapse: collapse; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
      thead {{ background: var(--panel); }}
      th, td {{ text-align: left; padding: 12px 10px; border-bottom: 1px solid var(--border); font-size: 14px; }}
      th {{ font-size: 13px; color: var(--muted); font-weight: 700; }}
      .badge {{ display: inline-flex; align-items: center; padding: 4px 8px; border-radius: 999px; font-weight: 700; font-size: 12px; border: 1px solid transparent; }}
      .badge.high {{ color: var(--danger); background: rgba(220, 38, 38, 0.08); border-color: rgba(220, 38, 38, 0.2); }}
      .badge.medium {{ color: #b45309; background: rgba(245, 158, 11, 0.12); border-color: rgba(245, 158, 11, 0.2); }}
      .badge.low {{ color: var(--success); background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.2); }}
      .muted {{ color: var(--muted); }}
    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>Gestión de Pacientes — Sala de Emergencias</h1>
        <div class="stats">Total de pacientes: {count}</div>
      </header>

      <div class="grid">
        <section class="card">
          <h2>Agregar paciente</h2>
          <form method="post" action="{UI_ADD_END_ROUTE}">
            <div class="form-row cols-3">
              <div>
                <label for="patientName">Nombre del paciente</label>
                <input id="patientName" name="name" type="text" placeholder="Ej: Carlos Mendoza" required />
              </div>
              <div>
                <label for="patientAge">Edad</label>
                <input id="patientAge" name="age" type="number" min="1" placeholder="Ej: 45" required />
              </div>
              <div>
                <label for="patientPriority">Prioridad</label>
                <select id="patientPriority" name="priority">
                  <option value="{PRIORITY_HIGH}">{PRIORITY_HIGH}</option>
                  <option value="{PRIORITY_MEDIUM}" selected>{PRIORITY_MEDIUM}</option>
                  <option value="{PRIORITY_LOW}">{PRIORITY_LOW}</option>
                </select>
              </div>
            </div>

            <div class="actions">
              <button class="primary" type="submit">Agregar al final</button>
              <button class="primary" type="submit" formaction="{UI_ADD_START_ROUTE}">Agregar al inicio</button>
            </div>
          </form>

          <div class="message {message_class}">{message_text}</div>
        </section>

        <section class="card">
          <h2>Insertar en posición</h2>
          <form method="post" action="{UI_INSERT_ROUTE}">
            <div class="form-row cols-2">
              <div>
                <label for="insertIndex">Posición</label>
                <input id="insertIndex" name="index" type="number" min="0" placeholder="Ej: 0" required />
              </div>
              <div class="muted" style="display:flex;align-items:end;">
                Usa los mismos datos del formulario de “Agregar paciente”.
              </div>
            </div>
            <div class="actions">
              <button class="primary" type="submit">Insertar en posición</button>
            </div>
          </form>
        </section>
      </div>

      <section class="card">
        <h2>Lista de pacientes</h2>
        <table>
          <thead>
            <tr>
              <th style="width: 60px">#</th>
              <th>Nombre</th>
              <th style="width: 90px">Edad</th>
              <th style="width: 110px">Prioridad</th>
              <th style="width: 140px">Hora de llegada</th>
              <th style="width: 120px">Acción</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </section>
    </div>
  </body>
</html>
"""
    return HTMLResponse(content=html)


def _make_patient_payload(*, name: str, age: int, priority: str) -> dict[str, object]:
    """Create a patient dictionary with generated id and arrival time."""
    patient_id = int(time() * 1000)
    arrival_time = datetime.now().strftime("%H:%M:%S")
    return {"id": patient_id, "name": name, "age": age, "priority": priority, "arrival_time": arrival_time}


def _redirect_with_message(*, message: str, kind: Literal["success", "error"]) -> RedirectResponse:
    """Redirect back to the UI with a short Spanish status message."""
    return RedirectResponse(url=f"{UI_ROUTE}?message={quote(message)}&kind={kind}", status_code=303)


@router.post(UI_ADD_END_ROUTE, include_in_schema=False)
def ui_add_end(name: str = Form(...), age: int = Form(...), priority: str = Form(...)) -> RedirectResponse:
    """Handle the form action to append a patient to the queue."""
    try:
        payload = _make_patient_payload(name=name, age=age, priority=priority)
        patient_service.add_to_end(patient=payload)
        return _redirect_with_message(message="Paciente agregado al final.", kind="success")
    except PatientServiceError as exc:
        return _redirect_with_message(message=str(exc), kind="error")
    except Exception:
        return _redirect_with_message(message=MESSAGE_UNEXPECTED_ERROR, kind="error")


@router.post(UI_ADD_START_ROUTE, include_in_schema=False)
def ui_add_start(name: str = Form(...), age: int = Form(...), priority: str = Form(...)) -> RedirectResponse:
    """Handle the form action to prepend a patient to the queue."""
    try:
        payload = _make_patient_payload(name=name, age=age, priority=priority)
        patient_service.add_to_start(patient=payload)
        return _redirect_with_message(message="Paciente agregado al inicio.", kind="success")
    except PatientServiceError as exc:
        return _redirect_with_message(message=str(exc), kind="error")
    except Exception:
        return _redirect_with_message(message=MESSAGE_UNEXPECTED_ERROR, kind="error")


@router.post(UI_INSERT_ROUTE, include_in_schema=False)
def ui_insert(
    index: int = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    priority: str = Form(...),
) -> RedirectResponse:
    """Handle the form action to insert a patient at a specific index."""
    try:
        payload = _make_patient_payload(name=name, age=age, priority=priority)
        patient_service.insert_at_index(index=index, patient=payload)
        return _redirect_with_message(message="Paciente insertado en la posición indicada.", kind="success")
    except PatientServiceError as exc:
        return _redirect_with_message(message=str(exc), kind="error")
    except Exception:
        return _redirect_with_message(message=MESSAGE_UNEXPECTED_ERROR, kind="error")


@router.post(UI_REMOVE_ROUTE, include_in_schema=False)
def ui_remove(index: int) -> RedirectResponse:
    """Handle the form action to remove a patient by index."""
    try:
        patient_service.remove_at_index(index=index)
        return _redirect_with_message(message="Paciente eliminado.", kind="success")
    except PatientServiceError as exc:
        return _redirect_with_message(message=str(exc), kind="error")
    except Exception:
        return _redirect_with_message(message=MESSAGE_UNEXPECTED_ERROR, kind="error")


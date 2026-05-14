# Hospital Patient Queue Manager (Doubly Linked List)

Aplicación de ejemplo para gestionar la cola de pacientes en una sala de emergencias usando una **Lista Doblemente Enlazada** como estructura central.

Incluye:

- Backend en Python (FastAPI) con API REST.
- Interfaz web servida por el backend (UI en `http://127.0.0.1:8000/` y `http://127.0.0.1:8000/ui`).

## Cómo ejecutar

### 1) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2) Iniciar el backend (FastAPI)

Desde la carpeta `hospital_queue`:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

El backend queda disponible en:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/ui

### 3) Abrir la interfaz

Abre en el navegador:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/ui

## Endpoints

- `GET /patients` — obtener todos los pacientes
- `POST /patients` — agregar al final
- `POST /patients/prepend` — agregar al inicio
- `POST /patients/insert/{index}` — insertar en una posición
- `DELETE /patients/{index}` — eliminar por posición
- `GET /patients/count` — total de pacientes

## Estructura

```
hospital_queue/
  backend/
    main.py
    models/
      node.py
    structures/
      doubly_linked_list.py
    services/
      patient_service.py
    routes/
      patient_routes.py
  requirements.txt
  README.md
```

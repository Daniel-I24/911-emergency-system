# 🏥 Sistema de Gestión de Emergencias 911

> API REST para gestión de cola de pacientes en salas de emergencia usando **Lista Doblemente Enlazada**.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

## 🎯 Descripción

Sistema de cola de pacientes que utiliza una **Lista Doblemente Enlazada** para operaciones eficientes:
- Inserción/Eliminación O(1) en extremos
- Navegación bidireccional optimizada
- Gestión flexible por prioridad

## ✨ Características

- API RESTful con FastAPI
- Validación de datos y prevención de duplicados
- Gestión de prioridades (Alta, Media, Baja)
- Documentación automática (Swagger UI)
- Interfaz web integrada

## 🚀 Instalación Rápida

```bash
# Clonar e instalar
git clone <url-del-repositorio>
cd 911-emergency-system
pip install -r requirements.txt

# Iniciar servidor
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**URLs importantes:**
- API: http://127.0.0.1:8000/
- Documentación: http://127.0.0.1:8000/docs
- Interfaz web: http://127.0.0.1:8000/ui

## 🏗️ Arquitectura

```
backend/
├── main.py                      # Punto de entrada
├── models/node.py              # Nodo de lista enlazada
├── structures/                 # Lista doblemente enlazada
├── services/                   # Lógica de negocio
└── routes/                     # Endpoints API
```

**Capas:**
- **Routes**: Manejo de peticiones HTTP
- **Services**: Validación y reglas de negocio
- **Structures**: Implementación de lista enlazada
- **Models**: Estructuras de datos básicas

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/patients` | Obtener todos los pacientes |
| `POST` | `/patients` | Agregar al final |
| `POST` | `/patients/prepend` | Agregar al inicio (urgente) |
| `POST` | `/patients/insert/{index}` | Insertar en posición |
| `DELETE` | `/patients/{index}` | Eliminar por posición |
| `GET` | `/patients/count` | Total de pacientes |

## 📊 Modelo de Datos

```json
{
  "id": 1,
  "name": "Juan Pérez",
  "age": 45,
  "priority": "Alta",
  "arrival_time": "2024-01-15 10:30:00"
}
```

**Validaciones:**
- `id`: Entero único
- `name`: String no vacío
- `age`: Entero > 0
- `priority`: "Alta", "Media" o "Baja"
- `arrival_time`: String de fecha/hora

## 💡 Ejemplos de Uso

### cURL
```bash
# Agregar paciente
curl -X POST "http://127.0.0.1:8000/patients" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"name":"Juan Pérez","age":45,"priority":"Alta","arrival_time":"2024-01-15 10:30:00"}'

# Obtener todos
curl -X GET "http://127.0.0.1:8000/patients"
```

### Python
```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Agregar paciente
patient = {"id": 1, "name": "Juan Pérez", "age": 45, "priority": "Alta", "arrival_time": "2024-01-15 10:30:00"}
response = requests.post(f"{BASE_URL}/patients", json=patient)
print(response.json())
```

### JavaScript
```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Agregar paciente
const patient = {id: 1, name: "Juan Pérez", age: 45, priority: "Alta", arrival_time: "2024-01-15 10:30:00"};
const response = await fetch(`${BASE_URL}/patients`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify(patient)
});
const data = await response.json();
```

## 🔗 Complejidad Algorítmica

| Operación | Complejidad | Descripción |
|-----------|-------------|-------------|
| `append()` | O(1) | Agregar al final |
| `prepend()` | O(1) | Agregar al inicio |
| `insert(index)` | O(n) | Insertar en posición |
| `remove(index)` | O(n) | Eliminar por índice |
| `find_by_id()` | O(n) | Buscar por ID |
| `get_length()` | O(1) | Obtener tamaño |

**Optimización:** El método `_node_at()` recorre desde el extremo más cercano (head o tail), reduciendo el tiempo promedio a O(n/2).

## 🛡️ Manejo de Errores

```json
// Datos inválidos
{"success": false, "data": null, "message": "Datos del paciente incompletos o inválidos."}

// ID duplicado
{"success": false, "data": null, "message": "Ya existe un paciente con ese ID."}

// Índice inválido
{"success": false, "data": null, "message": "Índice inválido."}
```

## 🧪 Testing

- **Swagger UI**: http://127.0.0.1:8000/docs (recomendado)
- **Interfaz Web**: http://127.0.0.1:8000/ui
- **Herramientas**: cURL, Postman, HTTPie

## 📝 Licencia

MIT License

---

**¿Preguntas?** Abre un issue en el repositorio.

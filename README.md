# Sistema de Emergencias 911

Simulación de un centro de llamadas de emergencia 911. Un operador recibe llamadas, las prioriza por gravedad, asigna la unidad de respuesta más cercana, sigue un protocolo paso a paso y puede deshacer acciones.

---

## Características

- **Cola de prioridad** para las llamadas de emergencia, de modo que el incidente más grave siempre se atiende primero.
- **Algoritmo de Dijkstra** para encontrar la unidad de respuesta disponible más cercana según la distancia por carretera.
- **Árbol de decisión** que guía al operador por el protocolo correcto según el tipo de incidente.
- **Lista enlazada simple** que guarda el historial de despachos.
- **Arreglo circular** para rotar la selección de unidades cuando dos están a la misma distancia.
- **Pila** para deshacer la última acción.
- **Cola** para el registro de eventos en tiempo real.
- **Aplicación de escritorio** con interfaz gráfica en Tkinter.

---

## Estructuras de datos

| Estructura | Uso |
|-----------|-----|
| Cola de prioridad (min-heap) | Ordenar las llamadas entrantes por gravedad |
| Grafo + Dijkstra | Calcular la distancia más corta por carretera a cada unidad |
| Árbol de decisión | Preguntas de protocolo según el tipo de incidente |
| Lista enlazada simple | Historial cronológico de despachos |
| Arreglo circular | Rotación de unidades para desempatar |
| Pila (LIFO) | Deshacer la acción más reciente |
| Cola (FIFO) | Registro de eventos en orden |
| Lista de Python | Colecciones internas |

---

## Cómo funciona

1. Llega una llamada y se agrega a la **cola de prioridad** según su gravedad.
2. El operador sigue el **árbol de decisión** correspondiente al tipo de incidente.
3. **Dijkstra** calcula las distancias por carretera desde el incidente hasta las unidades disponibles. Si hay empate, el **arreglo circular** decide cuál despachar.
4. El despacho se agrega al **historial** (lista enlazada) y el evento se registra en la **cola de eventos**.
5. Si el operador se equivoca, la **pila** deshace la última acción.

---

## Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones de Python)

En Debian/Ubuntu, si Tkinter no está instalado:

```bash
sudo apt install python3-tk
```

---

```
emergency-system/
├── app.py                          # Punto de entrada: inicia la interfaz Tkinter
├── backend/
│   ├── models/
│   │   ├── node.py                 # Nodo del grafo (ubicación)
│   │   └── emergency.py            # Modelo de llamada de emergencia
│   ├── structures/
│   │   ├── circular_array.py       # Rotación justa de unidades
│   │   ├── decision_tree.py        # Lógica de protocolos del operador
│   │   ├── graph.py                # Red vial de la ciudad + Dijkstra
│   │   ├── priority_queue.py       # Llamadas ordenadas por gravedad
│   │   ├── queue.py                # Registro FIFO de eventos
│   │   ├── singly_linked_list.py   # Historial de despachos
│   │   └── stack.py                # Pila para deshacer
│   └── services/
│       └── emergency_service.py    # Coordina las estructuras anteriores
├── requirements.txt
└── README.md
```

---

## Complejidad

| Operación | Estructura | Complejidad temporal |
|-----------|-----------|----------------------|
| Agregar emergencia | Cola de prioridad | O(log n) |
| Encontrar unidad más cercana | Dijkstra | O((V + E) log V) |
| Deshacer última acción | Pila | O(1) |
| Registrar evento | Cola | O(1) |
| Agregar registro de despacho | Lista enlazada | O(1) (se inserta al inicio) |
| Recorrer todo el historial | Lista enlazada | O(n) |
| Obtener la siguiente unidad en la rotación | Arreglo circular | O(1) |

---

## Justificación de las estructuras

**Cola de prioridad:** Un paro cardíaco debe despacharse antes que una queja por ruido. Un min-heap mantiene la llamada más grave al frente, sin necesidad de revisar toda la lista.

**Dijkstra sobre un grafo:** La ciudad se modela como un grafo ponderado de ubicaciones y calles. "Más cercano" se mide por distancia real de carretera, no en línea recta.

**Árbol de decisión:** Cada tipo de incidente requiere preguntas distintas (por ejemplo, "¿El paciente respira?"). El árbol mantiene al operador en el protocolo correcto y evita saltarse pasos.

**Lista enlazada simple:** El historial solo se recorre en secuencia, así que una lista enlazada permite insertar en O(1) sin necesidad de acceso aleatorio.

**Arreglo circular:** Rotar entre unidades empatadas reparte el trabajo de forma equitativa, y cada unidad recibe su turno antes de que alguna se repita.

**Pila:** "Deshacer lo último que se hizo" corresponde exactamente al orden LIFO.

**Cola:** Los eventos se muestran en el orden en que ocurrieron. Encolar y desencolar son O(1).

---

## Tecnologías

- Python 3
- Tkinter (interfaz gráfica)
- Estructuras de datos propias (sin librerías externas pesadas)

# 911 Emergency System

A desktop simulation of a 911 emergency call center. An operator takes incoming calls, prioritizes them by severity, dispatches the nearest available response unit, follows a protocol step by step, and can undo mistakes.

---

## Features

- **Priority queue** for emergency calls, so the most severe incident is always handled first.
- **Dijkstra's algorithm** to find the nearest available response unit by road distance.
- **Decision tree** that guides the operator through the right protocol for each incident type.
- **Singly linked list** that stores the dispatch history.
- **Circular array** for fair unit rotation when two units are equally close.
- **Stack** for undoing the last action.
- **Queue** for real-time event logging.
- **Tkinter GUI** desktop application.

---

## Data Structures

| Structure | Used for |
|-----------|----------|
| Priority Queue (min-heap) | Ordering incoming calls by severity |
| Graph + Dijkstra | Finding the shortest road distance to each unit |
| Decision Tree | Branching protocol questions by incident type |
| Singly Linked List | Chronological dispatch history |
| Circular Array | Rotating unit selection to break ties |
| Stack (LIFO) | Undo of the most recent action |
| Queue (FIFO) | In-order event log |
| Python list | Internal collections |

---

## How It Works

1. A call comes in and is added to the **priority queue** by severity.
2. The operator follows the **decision tree** for that incident type.
3. **Dijkstra** computes road distances from the incident to the available units. If units are tied, the **circular array** decides which one to dispatch.
4. The dispatch is added to the **linked list** history, and the event is recorded in the **event queue**.
5. If the operator makes a mistake, the **stack** undoes the last action.

---

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

On Debian/Ubuntu, if Tkinter is missing:

```bash
sudo apt install python3-tk
```

---

## Getting Started

```bash
cd emergency-system
python app.py
```

---

## Project Structure

```
emergency-system/
├── app.py                          # Entry point: launches the Tkinter GUI
├── backend/
│   ├── models/
│   │   ├── node.py                 # Graph node (location)
│   │   └── emergency.py            # Emergency call model
│   ├── structures/
│   │   ├── circular_array.py       # Fair unit rotation
│   │   ├── decision_tree.py        # Operator protocol logic
│   │   ├── graph.py                # City road network + Dijkstra
│   │   ├── priority_queue.py       # Calls ordered by severity
│   │   ├── queue.py                # FIFO event log
│   │   ├── singly_linked_list.py   # Dispatch history
│   │   └── stack.py                # Undo stack
│   └── services/
│       └── emergency_service.py    # Coordinates the structures above
├── requirements.txt
└── README.md
```

---

## Complexity

| Operation | Data Structure | Time Complexity |
|-----------|----------------|-----------------|
| Add emergency | Priority Queue | O(log n) |
| Find nearest unit | Dijkstra | O((V + E) log V) |
| Undo last action | Stack | O(1) |
| Log event | Queue | O(1) |
| Add dispatch record | Singly Linked List | O(1) (inserted at head) |
| Read full history | Singly Linked List | O(n) |
| Get next unit in rotation | Circular Array | O(1) |

---

## Design Rationale

**Priority Queue:** A cardiac arrest must be dispatched before a noise complaint. A min-heap keeps the most severe call on top, so the next call is found without scanning the whole list.

**Dijkstra on a Graph:** The city is a weighted graph of locations and roads. "Nearest" is measured by road distance, not a straight line on the map.

**Decision Tree:** Each incident type needs different questions (e.g., "Is the patient breathing?"). The tree keeps the operator on the correct protocol and prevents skipped steps.

**Singly Linked List:** The history is only read sequentially, so a linked list gives O(1) inserts without needing random access.

**Circular Array:** Cycling through tied units spreads work evenly, and every unit gets a turn before any unit repeats.

**Stack:** "Undo the last thing done" is exactly LIFO order.

**Queue:** Events are displayed in the order they happened. Enqueue and dequeue are both O(1).

---

## Tech Stack

- Python 3
- Tkinter (GUI)
- Custom data structures (no heavy external libraries)

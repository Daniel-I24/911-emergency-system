# 911 Emergency System (Python)

Simulation of a 911 emergency call center: intake calls, prioritize them, pick the nearest available response unit using Dijkstra, guide the operator with a decision tree, keep a linked history, rotate unit selection, and allow undo.

Data structures used in the project:

- Stack (LIFO) for undo actions.
- Queue (FIFO) for an in-memory event stream.
- List (Python list) for internal collections.
- Singly Linked List for the dispatch history.

## How to run

This project runs as a desktop application using Tkinter.

```bash
python app.py
```

## Features

-Priority Queue for handling emergency calls by severity
-Dijkstra’s Algorithm to find the nearest available response unit
-Decision Tree to guide operators according to incident type
-Singly Linked List for dispatch history
-Circular Array for fair unit selection rotation (tie-breaking)
-Stack for Undo last action
-Queue for real-time event logging
-Complete Tkinter GUI desktop application


## Tech Stack

Python 3
Tkinter – Graphical User Interface
Custom Data Structures (no external heavy libraries)

## Complexity Analysis
| Operation | Data Structure | Time Complexity |
|-----------|---------------|-----------------|
| Add emergency | Priority Queue | O(log n) |
| Find nearest unit | Dijkstra | O((V + E) log V) |
| Undo action | Stack | O(1) |
| Log event | Queue | O(1) |
| Dispatch history | Singly Linked List | O(n) |
| Unit rotation | Circular Array | O(1) |

## Structure

```
emergency-system/
  app.py
  backend/
    models/
      node.py
      emergency.py
    structures/
      circular_array.py
      decision_tree.py
      graph.py
      priority_queue.py
      queue.py
      singly_linked_list.py
      stack.py
    services/
      emergency_service.py
  requirements.txt
  README.md
```


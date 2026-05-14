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

- Create emergency calls and prioritize them (priority queue)
- Dispatch the next call to the nearest available unit (Dijkstra)
- Operator guide by incident type (decision tree)
- Dispatch history stored in a linked list
- Unit selection rotation for tie-breaks (circular array)
- Undo last action (stack).

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

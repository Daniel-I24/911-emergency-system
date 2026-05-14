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

## Why These Data Structures?

### Priority Queue — handling calls by severity
Emergency calls are not equal. A cardiac arrest must be dispatched before a noise complaint. A priority queue (backed by a min-heap) keeps the highest-severity call at the top at all times, so the dispatcher always processes the most critical incident next without scanning the entire list. Inserting or extracting a call costs O(log n), which is fast even under high call volume.

### Dijkstra's Algorithm on a Graph — finding the nearest unit
The city is modeled as a weighted graph where nodes are locations and edges are roads with travel distances. When a call comes in, Dijkstra computes the shortest path from every available unit to the incident site, so the closest one gets dispatched. This solves the real-world constraint that "nearest" means road distance, not a straight line on a map.

### Decision Tree — guiding the operator
Different emergencies require different questions (Is the patient breathing? Is the fire contained?). A decision tree encodes this branching logic so the operator is walked through the correct protocol for each incident type. It removes guesswork under pressure and ensures no critical step is skipped.

### Singly Linked List — dispatch history
Every dispatch is appended to a linked list, forming a chronological log. New records are added in O(1) at the head, and the full history can be traversed in O(n). A linked list fits here because history only needs sequential access — random access by index is never required.

### Circular Array — fair unit rotation
When two units are equally close, the system needs a tie-breaker that prevents one unit from being overloaded. A circular array cycles through available units so selection wraps around evenly. Advancing the pointer is O(1) and guarantees every unit gets a turn before any unit repeats.

### Stack — undo last action
Operators make mistakes. A stack lets the system reverse the most recent dispatch action in O(1) by simply popping the top entry. The LIFO nature of a stack maps directly onto "undo the last thing done," making it the natural fit for this feature.

### Queue — real-time event log
System events (call received, unit dispatched, call resolved) are appended to a queue as they happen and consumed in order for display. The FIFO guarantee means events are shown in the exact sequence they occurred. Both enqueue and dequeue are O(1), so logging never slows down the rest of the system.

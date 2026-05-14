from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    to_node: str
    weight: int


class WeightedGraph:
    def __init__(self) -> None:
        self._adjacency: dict[str, list[Edge]] = {}

    def add_node(self, node: str) -> None:
        self._adjacency.setdefault(node, [])

    def add_undirected_edge(self, *, a: str, b: str, weight: int) -> None:
        if weight < 0:
            raise ValueError("Edge weight must be non-negative")
        self.add_node(a)
        self.add_node(b)
        self._adjacency[a].append(Edge(to_node=b, weight=weight))
        self._adjacency[b].append(Edge(to_node=a, weight=weight))

    def nodes(self) -> list[str]:
        return list(self._adjacency.keys())

    def dijkstra_distances(self, *, source: str) -> dict[str, int]:
        if source not in self._adjacency:
            raise ValueError("Unknown source node")

        unvisited = self.nodes()
        distances: dict[str, int] = {node: 10**12 for node in unvisited}
        distances[source] = 0

        while unvisited:
            current = min(unvisited, key=lambda n: distances[n])
            unvisited.remove(current)

            current_distance = distances[current]
            if current_distance >= 10**12:
                break

            for edge in self._adjacency.get(current, []):
                if edge.to_node not in distances:
                    continue
                candidate = current_distance + edge.weight
                if candidate < distances[edge.to_node]:
                    distances[edge.to_node] = candidate

        return distances


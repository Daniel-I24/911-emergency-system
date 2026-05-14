from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    """
    Representa una arista o conexión unidireccional entre dos nodos en un grafo.
    
    Attributes:
        to_node (str): El identificador del nodo de destino.
        weight (int): El peso o costo de recorrer esta arista.
    """
    to_node: str
    weight: int


class WeightedGraph:
    """
    Implementación de un grafo ponderado utilizando listas de adyacencia.
    """
    def __init__(self) -> None:
        """
        Inicializa un grafo ponderado vacío.
        """
        self._adjacency: dict[str, list[Edge]] = {}

    def add_node(self, node: str) -> None:
        """
        Agrega un nodo al grafo si no existe.
        
        Args:
            node (str): El identificador del nodo a agregar.
        """
        self._adjacency.setdefault(node, [])

    def add_undirected_edge(self, *, a: str, b: str, weight: int) -> None:
        """
        Agrega una arista no dirigida (bidireccional) entre dos nodos con un peso específico.
        
        Args:
            a (str): El primer nodo.
            b (str): El segundo nodo.
            weight (int): El peso de la arista (debe ser no negativo).
            
        Raises:
            ValueError: Si el peso es negativo.
        """
        if weight < 0:
            raise ValueError("Edge weight must be non-negative")
        self.add_node(a)
        self.add_node(b)
        self._adjacency[a].append(Edge(to_node=b, weight=weight))
        self._adjacency[b].append(Edge(to_node=a, weight=weight))

    def nodes(self) -> list[str]:
        """
        Devuelve una lista con todos los nodos presentes en el grafo.
        
        Returns:
            list[str]: Lista de identificadores de nodos.
        """
        return list(self._adjacency.keys())

    def dijkstra_distances(self, *, source: str) -> dict[str, int]:
        """
        Calcula las distancias más cortas desde un nodo de origen a todos los demás nodos
        en el grafo utilizando el algoritmo de Dijkstra.
        
        Args:
            source (str): El nodo de origen desde donde calcular las distancias.
            
        Returns:
            dict[str, int]: Un diccionario donde la clave es el nodo y el valor es la distancia más corta.
            
        Raises:
            ValueError: Si el nodo de origen no existe en el grafo.
        """
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


"""Общие кирпичики темы Graphs: узел графа и преобразования «словарь смежности <-> узлы».

Узел нужен только задаче о глубокой копии; остальные задачи получают граф
списком смежности, списком рёбер или матрицей.
"""

from __future__ import annotations

from collections import deque


class GraphNode:
    """Вершина неориентированного графа: значение и список соседей-узлов."""

    __slots__ = ("val", "neighbors")

    def __init__(self, val: int) -> None:
        self.val = val
        self.neighbors: list[GraphNode] = []

    def __repr__(self) -> str:
        return f"GraphNode({self.val})"


def build_graph(adjacency: dict[int, list[int]]) -> dict[int, GraphNode]:
    """Собрать граф из словаря «значение -> значения соседей».

    Возвращает словарь «значение -> узел», чтобы тест мог взять любую вершину
    как точку входа. Симметричность словаря — забота вызывающего.
    """
    nodes = {val: GraphNode(val) for val in adjacency}
    for val, neighbor_vals in adjacency.items():
        nodes[val].neighbors = [nodes[other] for other in neighbor_vals]
    return nodes


def collect_nodes(start: GraphNode | None) -> list[GraphNode]:
    """Все узлы, достижимые из start, в порядке обхода в ширину."""
    if start is None:
        return []
    found = [start]
    seen = {id(start)}          # id, а не val: нам важны именно объекты
    pending = deque([start])
    while pending:
        node = pending.popleft()
        for neighbor in node.neighbors:
            if id(neighbor) not in seen:
                seen.add(id(neighbor))
                found.append(neighbor)
                pending.append(neighbor)
    return found


def graph_to_adjacency(start: GraphNode | None) -> dict[int, list[int]]:
    """Обратное преобразование: узлы -> словарь «значение -> значения соседей»."""
    return {
        node.val: [neighbor.val for neighbor in node.neighbors]
        for node in collect_nodes(start)
    }

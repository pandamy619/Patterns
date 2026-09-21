"""Глубокая копия неориентированного графа по ссылке на одну из его вершин.

Приём: DFS (обход в глубину) + словарь «оригинал -> копия», который
одновременно служит отметкой «уже посещён».
Аналог: LeetCode 133.
"""

from __future__ import annotations

from graphs_helpers import GraphNode


def graph_deep_copy(node: GraphNode | None) -> GraphNode | None:
    """Вернуть копию вершины node, связанную с копиями всех остальных вершин.

    Время O(n + e), память O(n): словарь копий и стек рекурсии.
    """
    clones: dict[GraphNode, GraphNode] = {}

    def clone(original: GraphNode) -> GraphNode:
        # Копия уже есть — возвращаем её же. Без этого цикл a - b - a
        # уводит рекурсию в бесконечность, а у вершины с двумя путями
        # до неё появились бы две разные копии.
        if original in clones:
            return clones[original]

        copy = GraphNode(original.val)
        # Регистрируем копию ДО обхода соседей: сосед вернётся к нам
        # по обратному ребру и должен найти уже готовый объект.
        clones[original] = copy
        for neighbor in original.neighbors:
            copy.neighbors.append(clone(neighbor))
        return copy

    return clone(node) if node is not None else None

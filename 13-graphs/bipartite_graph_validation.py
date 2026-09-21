"""Является ли неориентированный граф двудольным.

graph[i] — список соседей вершины i. Граф двудольный, если вершины можно
покрасить в два цвета так, чтобы концы каждого ребра были разного цвета.
Приём: BFS (обход в ширину) с раскраской; DFS подошёл бы точно так же.
Аналог: LeetCode 785.
"""

from collections import deque

UNCOLORED = 0


def bipartite_graph_validation(graph: list[list[int]]) -> bool:
    """True, если граф можно правильно покрасить в два цвета.

    Время O(n + e), память O(n).
    """
    colors = [UNCOLORED] * len(graph)       # цвета: 1 и -1, смена цвета — умножение на -1

    for start in range(len(graph)):
        # Граф может состоять из нескольких кусков, поэтому обход
        # запускаем из каждой ещё не покрашенной вершины.
        if colors[start] != UNCOLORED:
            continue
        # Цвет первой вершины компоненты можно выбрать любым: вторая
        # допустимая раскраска компоненты — зеркальная, других нет.
        colors[start] = 1
        pending = deque([start])
        while pending:
            node = pending.popleft()
            for neighbor in graph[node]:
                if colors[neighbor] == UNCOLORED:
                    colors[neighbor] = -colors[node]
                    pending.append(neighbor)
                elif colors[neighbor] == colors[node]:
                    # Цвет соседа был вынужденным, и он совпал с нашим:
                    # значит, в графе есть цикл нечётной длины.
                    return False
    return True

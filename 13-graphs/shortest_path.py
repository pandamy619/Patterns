"""Кратчайшие расстояния от стартовой вершины до всех остальных во взвешенном графе.

Рёбра [u, v, w] неориентированные, веса неотрицательные; недостижимым
вершинам соответствует -1.
Приём: Dijkstra (алгоритм Дейкстры) с кучей и «ленивым» удалением.
Близкий аналог: LeetCode 743 (там граф ориентированный и нужен только максимум).
"""

import heapq
import sys

INFINITY = sys.maxsize


def shortest_path(n: int, edges: list[list[int]], start: int) -> list[int]:
    """Список из n расстояний от start; -1 для недостижимых вершин.

    Время O((n + e) * log n), память O(n + e).
    """
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    distance = [INFINITY] * n
    distance[start] = 0
    heap = [(0, start)]                 # (расстояние, вершина): куча сортирует по расстоянию
    while heap:
        dist, node = heapq.heappop(heap)
        # Устаревшая запись: пока она лежала в куче, нашёлся путь короче.
        # В heapq нет decrease-key, поэтому не обновляем записи, а пропускаем лишние.
        if dist > distance[node]:
            continue
        # Здесь dist окончательно: все прочие кандидаты в куче не ближе,
        # а неотрицательные рёбра не могут сделать путь через них короче.
        for neighbor, weight in adjacency[node]:
            candidate = dist + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    return [d if d != INFINITY else -1 for d in distance]

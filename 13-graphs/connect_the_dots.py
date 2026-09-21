"""Минимальная стоимость соединить все точки плоскости в одну сеть.

Стоимость отрезка между точками — манхэттенское расстояние |x1 - x2| + |y1 - y2|.
Приём: MST (минимальное остовное дерево). Основной вариант — алгоритм
Краскала на Union-Find, второй — алгоритм Прима для плотного графа.
Аналог: LeetCode 1584.
"""

from merging_communities import UnionFind


def _manhattan(a: list[int], b: list[int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def connect_the_dots(points: list[list[int]]) -> int:
    """Алгоритм Краскала: рёбра по возрастанию, берём те, что не замыкают цикл.

    Рёбер в полном графе n(n-1)/2, их сортировка доминирует:
    время O(n^2 * log n), память O(n^2).
    """
    n = len(points)
    edges = [
        (_manhattan(points[i], points[j]), i, j)
        for i in range(n)
        for j in range(i + 1, n)
    ]
    edges.sort()

    components = UnionFind(n)
    total = 0
    used = 0
    for cost, i, j in edges:
        # union вернёт False, если концы уже в одной компоненте: такое
        # ребро замкнуло бы цикл, а в цикле самое дорогое ребро лишнее.
        if components.union(i, j):
            total += cost
            used += 1
            if used == n - 1:           # дерево на n вершинах готово
                break
    return total


def connect_the_dots_prim(points: list[list[int]]) -> int:
    """Алгоритм Прима без кучи: растим одно дерево, каждый раз
    присоединяя ближайшую к нему точку.

    Время O(n^2), память O(n) — для полного графа это выгоднее Краскала,
    потому что рёбра не нужно ни хранить, ни сортировать.
    """
    n = len(points)
    if n == 0:
        return 0
    in_tree = [False] * n
    # closest[i] — цена самого дешёвого ребра от точки i до уже построенного дерева.
    closest = [_manhattan(points[0], point) for point in points]
    in_tree[0] = True
    total = 0
    for _ in range(n - 1):
        nearest = min(
            (i for i in range(n) if not in_tree[i]),
            key=lambda i: closest[i],
        )
        in_tree[nearest] = True
        total += closest[nearest]
        # В дереве появилась новая вершина — возможно, к кому-то она ближе прежних.
        for i in range(n):
            if not in_tree[i]:
                closest[i] = min(closest[i], _manhattan(points[nearest], points[i]))
    return total

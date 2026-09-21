"""Максимальная сумма непрерывного пути в бинарном дереве.

Путь — цепочка узлов, соединённых рёбрами, без развилок; начинаться и
заканчиваться может где угодно. Значения могут быть отрицательными.
Приём: postorder DFS, который возвращает одно («лучшая ветка вниз»),
а по дороге обновляет другое («лучший путь с изгибом в этом узле»).
Аналог: LeetCode 124.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode


def maximum_path_sum_in_a_binary_tree(root: Optional[TreeNode]) -> int:
    """Путь содержит хотя бы один узел, поэтому для дерева из одних
    отрицательных чисел ответ — наибольшее из них. Для пустого дерева — 0.

    Время O(n), память O(h).
    """
    if root is None:
        return 0
    best = root.val

    def best_branch(node: Optional[TreeNode]) -> int:
        """Лучшая сумма пути, который начинается в node и идёт только вниз."""
        nonlocal best
        if node is None:
            return 0
        # Отрицательная ветка только портит сумму — выгоднее её не брать вовсе.
        left = max(best_branch(node.left), 0)
        right = max(best_branch(node.right), 0)
        # Здесь узел — вершина «арки»: можно взять обе ветки сразу.
        best = max(best, node.val + left + right)
        # Родителю же отдаём только одну: путь через родителя не может
        # зайти в обе наши ветки — получилась бы развилка.
        return node.val + max(left, right)

    best_branch(root)
    return best

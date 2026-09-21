"""Ширина самого широкого уровня дерева.

Ширина уровня — расстояние между его крайними узлами, включая пустые
позиции между ними. Приём: BFS по уровням + нумерация позиций как в куче
(дети узла i — это 2i и 2i + 1).
Аналог: LeetCode 662.
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from trees_helpers import TreeNode


def widest_binary_tree_level(root: Optional[TreeNode]) -> int:
    """Максимум по уровням величины (правая позиция - левая позиция + 1).
    Для пустого дерева — 0.

    Время O(n), память O(w), w — наибольшее число узлов на уровне.
    """
    if root is None:
        return 0
    widest = 0
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    while queue:
        level_size = len(queue)
        leftmost = queue[0][1]
        rightmost = queue[-1][1]
        widest = max(widest, rightmost - leftmost + 1)
        for _ in range(level_size):
            node, position = queue.popleft()
            # Сдвигаем нумерацию так, чтобы левый край уровня был нулём.
            # Разности от этого не меняются, зато позиции не растут как 2^глубина:
            # в языках с фиксированным int это спасает от переполнения,
            # в Python — от арифметики над числами в тысячи бит.
            offset = position - leftmost
            if node.left:
                queue.append((node.left, 2 * offset))
            if node.right:
                queue.append((node.right, 2 * offset + 1))
    return widest

"""Проверить, что дерево сбалансировано по высоте.

Приём: postorder DFS — высота узла собирается из высот детей, а признак
«уже разбалансировано» поднимается наверх тем же возвращаемым значением.
Аналог: LeetCode 110.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode

_UNBALANCED = -1


def balanced_binary_tree_validation(root: Optional[TreeNode]) -> bool:
    """True, если в каждом узле высоты левого и правого поддеревьев
    отличаются не больше чем на 1. Пустое дерево сбалансировано.

    Время O(n): каждая высота считается ровно один раз. Память O(h).
    """
    return _height_or_flag(root) != _UNBALANCED


def _height_or_flag(node: Optional[TreeNode]) -> int:
    """Высота поддерева в узлах либо _UNBALANCED, если внутри есть перекос."""
    if node is None:
        return 0
    left = _height_or_flag(node.left)
    # Перекос найден — дальше считать незачем, просто несём флаг наверх.
    if left == _UNBALANCED:
        return _UNBALANCED
    right = _height_or_flag(node.right)
    if right == _UNBALANCED:
        return _UNBALANCED
    if abs(left - right) > 1:
        return _UNBALANCED
    return 1 + max(left, right)

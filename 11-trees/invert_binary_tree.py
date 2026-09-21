"""Зеркально отразить бинарное дерево.

Приём: DFS — в каждом узле меняем местами детей; порядок обхода не важен,
поэтому есть и рекурсивный, и итеративный (явный стек) вариант.
Аналог: LeetCode 226.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode


def invert_binary_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Рекурсивный вариант: отражает дерево на месте и возвращает корень.

    Время O(n), память O(h) на стек вызовов (h — высота, в худшем случае n).
    """
    if root is None:
        return None
    # Правая часть вычисляется целиком до присваивания, поэтому временная
    # переменная не нужна: оба поддерева уже отражены к моменту обмена.
    root.left, root.right = invert_binary_tree(root.right), invert_binary_tree(root.left)
    return root


def invert_binary_tree_iterative(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Итеративный вариант с явным стеком — не зависит от лимита рекурсии.

    Время O(n), память O(h) в среднем, O(n) в худшем случае.
    """
    pending: list[TreeNode] = [root] if root else []
    while pending:
        node = pending.pop()
        node.left, node.right = node.right, node.left
        # Обмен в узле не зависит от того, обработаны ли дети, так что
        # порядок извлечения из стека может быть любым.
        if node.left:
            pending.append(node.left)
        if node.right:
            pending.append(node.right)
    return root

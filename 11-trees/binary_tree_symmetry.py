"""Проверить, что дерево симметрично относительно вертикальной оси.

Приём: одновременный DFS по двум поддеревьям «в зеркальном порядке» —
левый ребёнок одного сравнивается с правым ребёнком другого.
Аналог: LeetCode 101.
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from trees_helpers import TreeNode


def binary_tree_symmetry(root: Optional[TreeNode]) -> bool:
    """Рекурсивный вариант. Пустое дерево симметрично.

    Время O(n), память O(h).
    """

    def mirrored(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if a is None or b is None:
            # Симметричны только если пусто с обеих сторон: форма тоже важна.
            return a is b
        return (
            a.val == b.val
            and mirrored(a.left, b.right)   # внешние края
            and mirrored(a.right, b.left)   # внутренние края
        )

    return root is None or mirrored(root.left, root.right)


def binary_tree_symmetry_iterative(root: Optional[TreeNode]) -> bool:
    """То же самое с очередью пар вместо рекурсии.

    Время O(n), память O(n) в худшем случае.
    """
    if root is None:
        return True
    pairs: deque[tuple[Optional[TreeNode], Optional[TreeNode]]] = deque(
        [(root.left, root.right)]
    )
    while pairs:
        a, b = pairs.popleft()
        if a is None and b is None:
            continue
        if a is None or b is None or a.val != b.val:
            return False
        pairs.append((a.left, b.right))
        pairs.append((a.right, b.left))
    return True

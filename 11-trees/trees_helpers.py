"""Общие вспомогательные вещи для темы Trees: узел дерева, сборка и сериализация.

Формат списка — «по уровням», как принято на LeetCode: значения идут слева
направо уровень за уровнем, None означает «здесь ребёнка нет», а у пустых мест
собственных детей в списке уже не бывает.

        5
       / \
      2   8          <->   [5, 2, 8, None, 3]
       \
        3

Обе функции работают через очередь, без рекурсии: тесты строят и вырожденные
деревья на десятки тысяч узлов, где рекурсия в Python упёрлась бы в лимит.
"""

from __future__ import annotations

from collections import deque
from typing import Optional, Sequence


class TreeNode:
    """Узел бинарного дерева."""

    __slots__ = ("val", "left", "right")

    def __init__(
        self,
        val: int,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        # Только значение: рекурсивный repr на глубоком дереве сам уронит стек.
        return f"TreeNode({self.val!r})"


def build_tree(values: Sequence[Optional[int]]) -> Optional[TreeNode]:
    """Собирает дерево из списка «по уровням». Время O(n), память O(n)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    parents: deque[TreeNode] = deque([root])
    position = 1
    while parents and position < len(values):
        parent = parents.popleft()
        # На каждого родителя в списке отведено два места: левое и правое.
        for side in ("left", "right"):
            if position >= len(values):
                break
            value = values[position]
            position += 1
            if value is not None:
                child = TreeNode(value)
                setattr(parent, side, child)
                parents.append(child)
    return root


def to_level_list(root: Optional[TreeNode]) -> list[Optional[int]]:
    """Обратная операция к build_tree. Хвостовые None отбрасываются, поэтому
    два дерева равны по форме и значениям тогда и только тогда, когда равны
    их списки. Время O(n), память O(n).
    """
    result: list[Optional[int]] = []
    queue: deque[Optional[TreeNode]] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while result and result[-1] is None:
        result.pop()
    return result


def find_node(root: Optional[TreeNode], value: int) -> Optional[TreeNode]:
    """Первый при обходе в ширину узел с данным значением (или None)."""
    queue: deque[TreeNode] = deque([root] if root else [])
    while queue:
        node = queue.popleft()
        if node.val == value:
            return node
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return None

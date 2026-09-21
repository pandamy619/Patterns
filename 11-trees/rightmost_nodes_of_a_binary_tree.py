"""Значения самых правых узлов на каждом уровне («вид на дерево справа»).

Приём: BFS по уровням — последний узел уровня и есть ответ. Второй вариант —
DFS «сначала вправо»: первый узел, встреченный на новой глубине, самый правый.
Аналог: LeetCode 199.
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from trees_helpers import TreeNode


def rightmost_nodes_of_a_binary_tree(root: Optional[TreeNode]) -> list[int]:
    """BFS по уровням. Время O(n), память O(w), w — ширина самого широкого уровня."""
    result: list[int] = []
    queue: deque[TreeNode] = deque([root] if root else [])
    while queue:
        # Размер очереди фиксируем ДО цикла: внутри в неё уже попадают дети,
        # то есть узлы следующего уровня.
        level_size = len(queue)
        for position in range(level_size):
            node = queue.popleft()
            if position == level_size - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result


def rightmost_nodes_dfs(root: Optional[TreeNode]) -> list[int]:
    """DFS с приоритетом правого ребёнка. Время O(n), память O(h)."""
    result: list[int] = []

    def visit(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        # Длина ответа равна числу уже «открытых» уровней. Раз идём сначала
        # вправо, первым на новую глубину приходит именно самый правый узел.
        if depth == len(result):
            result.append(node.val)
        visit(node.right, depth + 1)
        visit(node.left, depth + 1)

    visit(root, 0)
    return result

"""Проверить, что дерево — корректное бинарное дерево поиска (BST).

Приём: preorder DFS с допустимым интервалом, который сужается при спуске.
Второй вариант — итеративный inorder: у BST он обязан строго возрастать.
Дубликаты считаем нарушением (строгие неравенства).
Аналог: LeetCode 98.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode


def binary_search_tree_validation(root: Optional[TreeNode]) -> bool:
    """Каждый узел обязан лежать строго внутри интервала, заданного ВСЕМИ
    предками, а не только родителем. Пустое дерево — корректное BST.

    Время O(n), память O(h).
    """

    def fits(node: Optional[TreeNode], low: Optional[int], high: Optional[int]) -> bool:
        if node is None:
            return True
        # None вместо ±inf: не нужно гадать о диапазоне значений.
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        # Влево идём — текущее значение становится потолком, вправо — полом.
        return fits(node.left, low, node.val) and fits(node.right, node.val, high)

    return fits(root, None, None)


def binary_search_tree_validation_inorder(root: Optional[TreeNode]) -> bool:
    """Итеративный inorder: значения должны идти строго по возрастанию.

    Время O(n), память O(h); рекурсии нет, глубокое дерево не страшно.
    """
    stack: list[TreeNode] = []
    previous: Optional[int] = None
    node = root
    while stack or node:
        # Спускаемся до упора влево, запоминая путь.
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if previous is not None and node.val <= previous:
            return False
        previous = node.val
        node = node.right
    return True

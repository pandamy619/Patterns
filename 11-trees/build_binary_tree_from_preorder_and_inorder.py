"""Восстановить бинарное дерево по обходам preorder и inorder.

Приём: preorder называет корень, inorder делит остальные узлы на левое
и правое поддерево. Хеш-таблица «значение -> индекс в inorder» убирает
линейный поиск корня, а указатель по preorder — копирование срезов.
Значения в дереве уникальны.
Аналог: LeetCode 105.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode


def build_binary_tree_from_preorder_and_inorder(
    preorder: list[int], inorder: list[int]
) -> Optional[TreeNode]:
    """Время O(n), память O(n) на таблицу индексов плюс O(h) на рекурсию."""
    if len(preorder) != len(inorder):
        raise ValueError("обходы должны быть одной длины")
    inorder_index = {value: index for index, value in enumerate(inorder)}
    if len(inorder_index) != len(inorder):
        raise ValueError("значения должны быть уникальны")
    next_root = 0  # позиция в preorder, откуда возьмём следующий корень

    def build(low: int, high: int) -> Optional[TreeNode]:
        """Строит поддерево из узлов inorder[low..high] включительно."""
        nonlocal next_root
        if low > high:
            return None
        value = preorder[next_root]
        next_root += 1
        middle = inorder_index[value]
        node = TreeNode(value)
        # Порядок принципиален: в preorder сразу за корнем идёт ВСЁ левое
        # поддерево, и только потом правое. Построив сначала левое, мы
        # оставим указатель ровно на корне правого.
        node.left = build(low, middle - 1)
        node.right = build(middle + 1, high)
        return node

    return build(0, len(inorder) - 1)

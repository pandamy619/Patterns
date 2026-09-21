"""Вертикальный обход: значения узлов по столбцам.

Корень стоит в столбце 0, левый ребёнок — на столбец левее, правый — правее.
Столбцы выводятся слева направо, внутри столбца — сверху вниз, а узлы одного
уровня — слева направо. Приём: BFS (он сам даёт нужный порядок внутри
столбца) + хеш-таблица «столбец -> значения».
Аналог: LeetCode 314 (близкая, но с другим правилом для совпадений — 987).
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Optional

from trees_helpers import TreeNode


def binary_tree_columns(root: Optional[TreeNode]) -> list[list[int]]:
    """Время O(n), память O(n). Сортировка не нужна: границы столбцов
    отслеживаем по ходу обхода.
    """
    if root is None:
        return []
    columns: defaultdict[int, list[int]] = defaultdict(list)
    leftmost = rightmost = 0
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    while queue:
        node, column = queue.popleft()
        # BFS посещает узлы сверху вниз и слева направо, поэтому простое
        # добавление в конец списка уже соблюдает порядок внутри столбца.
        # С DFS так не выйдет: он может прийти в столбец сначала глубоким узлом.
        columns[column].append(node.val)
        leftmost = min(leftmost, column)
        rightmost = max(rightmost, column)
        if node.left:
            queue.append((node.left, column - 1))
        if node.right:
            queue.append((node.right, column + 1))
    # Столбцы занимают сплошной отрезок: за один шаг номер меняется на 1,
    # так что пропусков между leftmost и rightmost не бывает.
    return [columns[column] for column in range(leftmost, rightmost + 1)]

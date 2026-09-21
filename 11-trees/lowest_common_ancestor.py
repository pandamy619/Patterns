"""Наименьший общий предок (LCA) двух узлов бинарного дерева.

Приём: postorder DFS — поддерево сообщает наверх, что оно нашло; узел,
в котором впервые сошлись обе находки, и есть ответ.
Аналог: LeetCode 236.
"""

from __future__ import annotations

from typing import Optional

from trees_helpers import TreeNode


def lowest_common_ancestor(
    root: Optional[TreeNode], first: TreeNode, second: TreeNode
) -> Optional[TreeNode]:
    """Самый глубокий узел, в поддереве которого лежат оба узла (узел считается
    предком самого себя). Предполагается, что first и second — разные узлы
    этого дерева; сравниваем по ссылке, а не по значению.

    Время O(n), память O(h).
    """
    if root is None:
        return None
    # Ниже можно не спускаться: если второй узел под нами — мы и есть LCA,
    # если нет — развилка случится выше, и там нужен только факт «тут найден один».
    if root is first or root is second:
        return root
    from_left = lowest_common_ancestor(root.left, first, second)
    from_right = lowest_common_ancestor(root.right, first, second)
    # Находки пришли с обеих сторон — искомые узлы впервые разошлись именно здесь.
    if from_left and from_right:
        return root
    # Иначе передаём наверх то, что есть: одиночную находку, готовый LCA или None.
    return from_left or from_right

"""Найти узел, с которого два односвязных списка становятся общими.

Приём: два указателя, которые в конце своего списка переходят на чужой.
Аналог: LeetCode 160.
"""

from __future__ import annotations

from linked_lists_helpers import ListNode


def linked_list_intersection(
    head_a: ListNode | None, head_b: ListNode | None
) -> ListNode | None:
    """Вернуть первый общий узел (сравниваются сами узлы, не значения) или None.

    Время O(n + m), память O(1).
    """
    walker_a, walker_b = head_a, head_b

    # Каждый проходит «свой список + чужой», то есть одинаковые n + m шагов.
    # Общий хвост у обоих маршрутов в конце, поэтому к нему они подходят
    # одновременно. Нет общего хвоста — одновременно станут None, и цикл
    # закончится по тому же условию.
    while walker_a is not walker_b:
        # Переходим, когда указатель стал None, а не когда next is None:
        # иначе непересекающиеся списки зациклят нас навсегда.
        walker_a = walker_a.next if walker_a is not None else head_b
        walker_b = walker_b.next if walker_b is not None else head_a
    return walker_a


def linked_list_intersection_hash_set(
    head_a: ListNode | None, head_b: ListNode | None
) -> ListNode | None:
    """Прямолинейный вариант: запомнить узлы первого списка в множестве.

    Время O(n + m), память O(n). Хорош как первое, самое простое решение.
    """
    # ListNode не переопределяет __eq__/__hash__, так что в множестве
    # узлы различаются по идентичности, а не по значению — это нам и нужно.
    seen: set[ListNode] = set()
    node = head_a
    while node is not None:
        seen.add(node)
        node = node.next

    node = head_b
    while node is not None:
        if node in seen:
            return node
        node = node.next
    return None

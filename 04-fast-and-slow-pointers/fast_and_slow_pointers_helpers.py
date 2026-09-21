"""Общие заготовки темы Fast and Slow Pointers: узел списка и сборка списков.

Модуль нужен решениям и тестам этой темы; из других тем его не импортируют.
"""

from __future__ import annotations

from typing import Iterable, Optional


class ListNode:
    """Узел односвязного списка."""

    __slots__ = ("val", "next")

    def __init__(self, val: int, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        # Соседей намеренно не печатаем: в зацикленном списке это бесконечная рекурсия.
        return f"ListNode({self.val})"


def build_list(values: Iterable[int], loop_to: Optional[int] = None) -> Optional[ListNode]:
    """Собрать список из значений и вернуть голову.

    Если задан loop_to, хвост замыкается на узел с этим индексом —
    получается список с циклом. loop_to=None даёт обычный список.
    """
    nodes = [ListNode(value) for value in values]
    for node, following in zip(nodes, nodes[1:]):
        node.next = following
    if loop_to is not None:
        if not 0 <= loop_to < len(nodes):
            raise ValueError("loop_to должен быть индексом существующего узла")
        nodes[-1].next = nodes[loop_to]
    return nodes[0] if nodes else None

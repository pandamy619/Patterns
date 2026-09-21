"""Вспомогательные сущности темы Heaps: узел односвязного списка
и пара функций, чтобы в тестах и примерах не собирать списки руками.
"""

from __future__ import annotations

from typing import Iterable, Optional


class ListNode:
    """Узел односвязного списка.

    Операторы сравнения намеренно НЕ определены: так узел обычно задан
    в условиях задач, и именно поэтому его нельзя класть в кучу
    «как есть» — см. combine_sorted_linked_lists.py.
    """

    __slots__ = ("val", "next")

    def __init__(self, val: int, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


def build_list(values: Iterable[int]) -> Optional[ListNode]:
    """Собрать связный список из значений; для пустого входа вернуть None."""
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_to_values(head: Optional[ListNode]) -> list[int]:
    """Выписать значения списка в обычный list."""
    values: list[int] = []
    while head is not None:
        values.append(head.val)
        head = head.next
    return values

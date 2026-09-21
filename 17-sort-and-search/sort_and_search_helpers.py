"""Вспомогательные сущности темы Sort and Search: узел односвязного списка
и конвертеры «список Python <-> связный список» для тестов и примеров.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


class ListNode:
    """Узел односвязного списка."""

    __slots__ = ("val", "next")

    def __init__(self, val: int, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


def build_list(values: Iterable[int]) -> ListNode | None:
    """Собрать односвязный список из значений и вернуть голову (None для пустого входа)."""
    # Фиктивный узел избавляет от отдельной ветки «список пока пуст».
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def iter_nodes(head: ListNode | None) -> Iterator[ListNode]:
    """Пройти по узлам вдоль ссылок next."""
    node = head
    while node is not None:
        yield node
        node = node.next


def to_values(head: ListNode | None) -> list[int]:
    """Значения узлов по порядку — удобно сравнивать в тестах."""
    return [node.val for node in iter_nodes(head)]

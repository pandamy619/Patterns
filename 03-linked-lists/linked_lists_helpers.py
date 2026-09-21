"""Общие кирпичики темы Linked Lists: узлы и преобразования «список Python <-> связный список».

Решения задач импортируют узлы отсюда, тесты — ещё и функции-конвертеры.
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


class MultiLevelNode:
    """Узел многоуровневого списка: кроме next есть child — голова вложенного списка."""

    __slots__ = ("val", "next", "child")

    def __init__(
        self,
        val: int,
        next: MultiLevelNode | None = None,
        child: MultiLevelNode | None = None,
    ) -> None:
        self.val = val
        self.next = next
        self.child = child

    def __repr__(self) -> str:
        return f"MultiLevelNode({self.val})"


def build_list(values: Iterable[int]) -> ListNode | None:
    """Собрать односвязный список из значений и вернуть голову (None для пустого входа)."""
    # Фиктивный узел избавляет от отдельной ветки «список пока пуст».
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def iter_nodes(head: ListNode | MultiLevelNode | None) -> Iterator:
    """Пройти по узлам вдоль ссылок next."""
    node = head
    while node is not None:
        yield node
        node = node.next


def to_values(head: ListNode | MultiLevelNode | None) -> list[int]:
    """Значения узлов по порядку — удобно сравнивать в тестах."""
    return [node.val for node in iter_nodes(head)]

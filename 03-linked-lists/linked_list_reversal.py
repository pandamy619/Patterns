"""Развернуть односвязный список на месте.

Приём: pointer rewiring (перестановка ссылок) — итеративно и рекурсивно.
Аналог: LeetCode 206.
"""

from __future__ import annotations

from linked_lists_helpers import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    """Итеративный разворот. Возвращает новую голову.

    Время O(n), память O(1).
    """
    prev: ListNode | None = None
    curr = head
    while curr is not None:
        # Порядок строк принципиален: сначала спасаем ссылку на остаток,
        # иначе после разворота стрелки до него будет не добраться.
        following = curr.next
        curr.next = prev
        prev = curr
        curr = following
    # curr ушёл за конец, значит prev стоит на бывшем хвосте — новой голове.
    return prev


def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    """Рекурсивный разворот. Возвращает новую голову.

    Время O(n), память O(n) — стек вызовов. В CPython глубина рекурсии
    по умолчанию около 1000, так что для длинных списков нужен итеративный вариант.
    """
    # Пустой список и список из одного узла уже «развёрнуты».
    if head is None or head.next is None:
        return head

    # Верим рекурсии: всё после head развёрнуто, new_head — бывший хвост.
    new_head = reverse_list_recursive(head.next)

    # head.next всё ещё указывает на своего старого соседа, а тот теперь
    # стоит в самом конце развёрнутой части. Цепляем head за ним.
    head.next.next = head
    # Без этой строки у двух узлов останутся стрелки друг на друга — цикл.
    head.next = None
    return new_head

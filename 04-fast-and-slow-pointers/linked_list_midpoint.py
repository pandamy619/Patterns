"""Средний узел односвязного списка за один проход.

Приём: midpoint — быстрый указатель идёт вдвое быстрее, и когда он
упирается в конец, медленный стоит посередине.
Аналог: LeetCode 876 (там тоже нужен второй из двух средних).
"""

from __future__ import annotations

from typing import Optional

from fast_and_slow_pointers_helpers import ListNode


def linked_list_midpoint(head: Optional[ListNode]) -> Optional[ListNode]:
    """Вернуть средний узел; при чётной длине — второй из двух средних.

    Для пустого списка возвращает None. Время O(n), память O(1).
    """
    slow = fast = head
    # Идём, пока у fast есть полный двойной шаг. При чётной длине fast
    # в конце «сваливается» в None, и этот последний шаг уводит slow
    # на второй средний узел.
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def linked_list_midpoint_first(head: Optional[ListNode]) -> Optional[ListNode]:
    """То же, но при чётной длине вернуть первый из двух средних.

    Время O(n), память O(1).
    """
    if head is None:
        return None
    slow = fast = head
    # Условие строже: fast обязан приземлиться на узел, а не в None.
    # При чётной длине последний шаг не выполняется, и slow остаётся левее.
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

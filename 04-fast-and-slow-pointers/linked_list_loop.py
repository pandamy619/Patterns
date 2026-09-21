"""Есть ли в односвязном списке цикл и где он начинается.

Приём: cycle detection (алгоритм Флойда, «черепаха и заяц») —
медленный указатель шагает на один узел, быстрый на два.
Аналог: LeetCode 141 (есть ли цикл) и LeetCode 142 (начало цикла).
"""

from __future__ import annotations

from typing import Optional

from fast_and_slow_pointers_helpers import ListNode


def _meeting_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """Узел, где быстрый указатель догнал медленный, или None, если цикла нет."""
    slow = fast = head
    # Проверяем обе ссылки: fast прыгает через узел, и оборваться список
    # может как на самом fast, так и сразу за ним.
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        # Сравниваем после шага: до первого шага оба стоят на голове,
        # и это совпадение ни о чём не говорит. Сравниваем узлы, а не значения.
        if slow is fast:
            return slow
    return None


def linked_list_loop(head: Optional[ListNode]) -> bool:
    """Вернуть True, если по ссылкам next можно ходить бесконечно.

    Время O(n), память O(1).
    """
    return _meeting_node(head) is not None


def linked_list_loop_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """Вернуть первый узел цикла или None, если цикла нет.

    Время O(n), память O(1).
    """
    meeting = _meeting_node(head)
    if meeting is None:
        return None
    # От головы до входа в цикл m шагов. От точки встречи до входа — тоже m
    # с точностью до целых кругов (доказательство в README). Поэтому два
    # указателя с одинаковой скоростью сойдутся ровно на входе.
    from_head, from_meeting = head, meeting
    while from_head is not from_meeting:
        from_head = from_head.next
        from_meeting = from_meeting.next
    return from_head

"""Удалить k-й с конца узел односвязного списка за один проход.

Приёмы: dummy node (фиктивный узел) + два указателя с разрывом в k шагов.
Аналог: LeetCode 19.
"""

from __future__ import annotations

from linked_lists_helpers import ListNode


def remove_kth_last_node(head: ListNode | None, k: int) -> ListNode | None:
    """Удалить k-й с конца узел (k = 1 — хвост) и вернуть голову.

    Если в списке меньше k узлов, он возвращается без изменений.
    Время O(n), память O(1).
    """
    if k < 1:
        raise ValueError("k должно быть не меньше 1")

    # Удалять, возможно, придётся саму голову, а у неё нет предыдущего узла.
    # Фиктивный узел перед головой делает этот случай обычным.
    dummy = ListNode(0, head)

    # Разведчик уходит вперёд на k узлов.
    scout = dummy
    for _ in range(k):
        scout = scout.next
        if scout is None:
            # Список короче k: удалять нечего.
            return head

    # Дальше идём в ногу. Когда разведчик встанет на хвост, между ним и
    # отстающим ровно k узлов — то есть отстающий стоит ПЕРЕД удаляемым.
    before = dummy
    while scout.next is not None:
        scout = scout.next
        before = before.next

    before.next = before.next.next
    # Не head: если удалили голову, head указывает на выброшенный узел.
    return dummy.next

"""Слить k отсортированных односвязных списков в один отсортированный.

Приём: k-way merge. В куче лежит по одному узлу — текущей «голове» — от
каждого непустого списка, наверху всегда наименьший из них.
Аналог: LeetCode 23.
"""

from __future__ import annotations

import heapq
from typing import Optional

from heaps_helpers import ListNode


def combine_sorted_linked_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """Вернуть голову объединённого списка. Узлы переиспользуются, новые не создаются.

    Время O(N log k), память O(k), где N — общее число узлов, k — число списков.
    """
    # Элемент кучи — кортеж (значение, номер списка, узел).
    # Номер списка — tie-breaker. Без него при равных значениях Python
    # пошёл бы сравнивать сами узлы, а ListNode не умеет «<» — TypeError.
    # Номер уникален среди элементов кучи (от каждого списка там не больше
    # одного узла), поэтому до третьего поля сравнение не доходит никогда.
    heap: list[tuple[int, int, ListNode]] = [
        (head.val, index, head)
        for index, head in enumerate(lists)
        if head is not None
    ]
    heapq.heapify(heap)

    dummy = ListNode(0)  # фиктивная голова избавляет от ветки «первый узел»
    tail = dummy
    while heap:
        _, index, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        # На место ушедшего узла приходит следующий из ТОГО ЖЕ списка:
        # только он мог быть «спрятан» за извлечённым.
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, index, node.next))

    return dummy.next

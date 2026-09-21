"""Отсортировать односвязный список по возрастанию.

Приём: merge sort (сортировка слиянием). Середину ищем быстрым и медленным
указателями, половины сортируем рекурсивно и сливаем перестановкой ссылок.
Рядом — восходящий (bottom-up) вариант без рекурсии, с памятью O(1).
Аналог: LeetCode 148.
"""

from __future__ import annotations

from sort_and_search_helpers import ListNode


def sort_linked_list(head: ListNode | None) -> ListNode | None:
    """Вернуть голову отсортированного списка; узлы не создаются, меняются только ссылки.

    Время O(n log n), память O(log n) — глубина рекурсии. Сортировка стабильна.
    """
    # Пустой список и список из одного узла уже отсортированы — это дно рекурсии.
    if head is None or head.next is None:
        return head

    right_head = _split_in_half(head)
    left_sorted = sort_linked_list(head)
    right_sorted = sort_linked_list(right_head)
    return _merge_sorted(left_sorted, right_sorted)


def sort_linked_list_bottom_up(head: ListNode | None) -> ListNode | None:
    """То же самое без рекурсии: сливаем куски длиной 1, 2, 4, ... пока кусок не накроет весь список.

    Время O(n log n), память O(1). Сортировка стабильна.
    """
    length = 0
    node = head
    while node is not None:
        length += 1
        node = node.next

    dummy = ListNode(0, head)
    width = 1
    while width < length:
        tail = dummy           # хвост уже собранной части текущего прохода
        rest = dummy.next      # ещё не обработанный остаток списка
        while rest is not None:
            left = rest
            right = _cut_after(left, width)
            rest = _cut_after(right, width)
            tail.next = _merge_sorted(left, right)
            # Доходим до конца слитого куска, чтобы следующий пришить за ним.
            # Это не больше 2 * width шагов, на асимптотику прохода не влияет.
            while tail.next is not None:
                tail = tail.next
        width *= 2
    return dummy.next


def _split_in_half(head: ListNode) -> ListNode:
    """Разорвать список (из двух и более узлов) посередине и вернуть голову правой половины."""
    slow = head
    # fast стартует на шаг впереди: тогда slow остановится на ПОСЛЕДНЕМ узле
    # левой половины, и связь можно разорвать без указателя «предыдущий».
    # Заодно список из двух узлов делится как 1 + 1, а не 2 + 0, —
    # иначе рекурсия никогда бы не закончилась.
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    right_head = slow.next
    slow.next = None
    return right_head


def _cut_after(head: ListNode | None, size: int) -> ListNode | None:
    """Отрезать от head кусок из size узлов и вернуть голову того, что осталось."""
    node = head
    for _ in range(size - 1):
        if node is None:
            break
        node = node.next
    if node is None:
        return None
    rest = node.next
    node.next = None
    return rest


def _merge_sorted(left: ListNode | None, right: ListNode | None) -> ListNode | None:
    """Слить два отсортированных списка в один, переставляя ссылки."""
    dummy = ListNode(0)
    tail = dummy
    while left is not None and right is not None:
        # «<=», а не «<»: при равенстве берём узел из левой половины,
        # поэтому равные значения сохраняют исходный порядок (стабильность).
        if left.val <= right.val:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next
        tail = tail.next
    # Один из списков закончился — остаток второго уже отсортирован, пришиваем целиком.
    tail.next = left if left is not None else right
    return dummy.next

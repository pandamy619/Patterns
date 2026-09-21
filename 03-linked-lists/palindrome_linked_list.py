"""Проверить, читается ли односвязный список одинаково в обе стороны.

Приёмы: быстрый и медленный указатели находят середину, затем pointer
rewiring (перестановка ссылок) разворачивает вторую половину.
Аналог: LeetCode 234.
"""

from __future__ import annotations

from linked_list_reversal import reverse_list
from linked_lists_helpers import ListNode


def palindrome_linked_list(head: ListNode | None) -> bool:
    """True, если значения узлов образуют палиндром. Список после вызова цел.

    Время O(n), память O(1).
    """
    # Шаг 1. Середина: fast идёт вдвое быстрее, и когда он упирается в конец,
    # slow стоит на начале второй половины (при нечётной длине — на центре).
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    # Шаг 2. Назад по односвязному списку не пройти — поэтому разворачиваем
    # вторую половину и читаем её «с конца» обычным проходом вперёд.
    second_half = reverse_list(slow)

    # Шаг 3. Цикл ведём по развёрнутой половине: она кончается на None ровно
    # тогда, когда сравнивать больше нечего. При нечётной длине центральный
    # узел под конец сравнится сам с собой — лишнее, но безвредное сравнение.
    left, right = head, second_half
    same = True
    while right is not None:
        if left.val != right.val:
            same = False
            break
        left = left.next
        right = right.next

    # Шаг 4. Возвращаем список в исходный вид: портить вход ради
    # ответа «да/нет» — плохой тон, вызывающий этого не ждёт.
    reverse_list(second_half)
    return same

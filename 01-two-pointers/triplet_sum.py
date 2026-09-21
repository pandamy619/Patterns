"""Все уникальные тройки с нулевой суммой.

Стратегия: сортировка + фиксируем один элемент + inward traversal по остатку.
Аналог: LeetCode 15.
"""


def triplet_sum(nums: list[int]) -> list[list[int]]:
    """Вернуть все тройки значений с суммой 0 без повторов.

    Время O(n^2), память O(1) сверх сортировки и ответа.
    """
    values = sorted(nums)
    n = len(values)
    result: list[list[int]] = []

    for first in range(n - 2):
        # Массив отсортирован: если первый элемент положительный,
        # два следующих тоже положительные — ноль уже не собрать.
        if values[first] > 0:
            break
        # Одинаковый первый элемент дал бы те же самые тройки.
        if first > 0 and values[first] == values[first - 1]:
            continue

        lo, hi = first + 1, n - 1
        while lo < hi:
            total = values[first] + values[lo] + values[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([values[first], values[lo], values[hi]])
                lo += 1
                hi -= 1
                # Пропускаем дубликаты второго элемента. Третий при этом
                # определяется однозначно, отдельно его проверять не нужно.
                while lo < hi and values[lo] == values[lo - 1]:
                    lo += 1
    return result

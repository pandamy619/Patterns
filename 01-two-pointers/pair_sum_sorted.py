"""Пара с заданной суммой в отсортированном массиве.

Стратегия: inward traversal (встречное движение).
Аналог: LeetCode 167 (там индексы с единицы, здесь — с нуля).
"""


def pair_sum_sorted(nums: list[int], target: int) -> list[int]:
    """Вернуть индексы любой пары с суммой target или [] — если пары нет.

    Время O(n), память O(1).
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        current = nums[lo] + nums[hi]
        if current == target:
            return [lo, hi]
        if current < target:
            # Сумму можно увеличить только сдвигом левого указателя:
            # правее lo значения не меньше.
            lo += 1
        else:
            hi -= 1
    return []

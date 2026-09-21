"""Пара с заданной суммой в неотсортированном массиве.

Идея: хеш-таблица «значение -> индекс», дополнение ищем за O(1).
Аналог: LeetCode 1.
"""


def pair_sum_unsorted(nums: list[int], target: int) -> list[int]:
    """Вернуть индексы любой пары с суммой target или [] — если пары нет.

    Время O(n), память O(n).
    """
    seen: dict[int, int] = {}  # значение -> индекс, где мы его встретили
    for index, value in enumerate(nums):
        complement = target - value
        # Сначала ищем, потом кладём: так элемент не составит пару сам с собой.
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    return []

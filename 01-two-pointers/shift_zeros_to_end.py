"""Сдвинуть нули в конец массива, сохранив порядок остальных элементов.

Стратегия: unidirectional traversal (однонаправленное движение).
Аналог: LeetCode 283.
"""


def shift_zeros_to_end(nums: list[int]) -> None:
    """Изменяет nums на месте. Время O(n), память O(1)."""
    write = 0  # сюда встанет следующий ненулевой элемент
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1

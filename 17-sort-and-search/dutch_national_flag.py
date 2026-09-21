"""Задача о флаге Нидерландов: массив из 0, 1 и 2 упорядочить на месте за один проход.

Приём: three-way partition (разбиение на три зоны) — то самое разбиение,
на котором в этой теме построены quicksort и quickselect, в чистом виде.
Аналог: LeetCode 75.
"""

from __future__ import annotations


def dutch_national_flag(nums: list[int]) -> None:
    """Переставить элементы nums (только 0, 1, 2) по возрастанию на месте.

    Время O(n) — один проход, память O(1).
    """
    low, i, high = 0, 0, len(nums) - 1
    # Слева от low — нули, между low и i — единицы, справа от high — двойки,
    # отрезок [i, high] ещё не разобран.
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[high] = nums[high], nums[i]
            high -= 1
            # i не двигаем: на его место приехал ещё не просмотренный элемент.
        elif nums[i] == 1:
            i += 1
        else:
            raise ValueError(f"ожидались только 0, 1 и 2, встретилось {nums[i]}")

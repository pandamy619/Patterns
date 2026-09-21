"""Наибольшая сумма непрерывного подмассива (алгоритм Кадане).

Приём: 1D DP, где состояние — «лучший подмассив, который ЗАКАНЧИВАЕТСЯ здесь».
Массив по условию непустой, пустой подмассив не считается.
Аналог: LeetCode 53.
"""


def maximum_subarray_sum(nums: list[int]) -> int:
    """Только сумма.

    Время O(n), память O(1).
    """
    if not nums:
        raise ValueError("массив должен быть непустым")
    # Стартуем с первого элемента, а не с нуля: иначе для массива
    # из одних отрицательных чисел получится 0 — сумма пустого подмассива.
    ending_here = best = nums[0]
    for value in nums[1:]:
        # Подмассив с концом в value либо продолжает предыдущий, либо начинается
        # заново. Продолжать выгодно ровно тогда, когда прежний хвост > 0.
        ending_here = max(value, ending_here + value)
        best = max(best, ending_here)
    return best


def maximum_subarray_with_bounds(nums: list[int]) -> tuple[int, int, int]:
    """Сумма и границы подмассива: (сумма, начало, конец), конец включительно.

    Время O(n), память O(1).
    """
    if not nums:
        raise ValueError("массив должен быть непустым")
    ending_here = best = nums[0]
    start = best_start = best_end = 0
    for index in range(1, len(nums)):
        if ending_here > 0:
            ending_here += nums[index]
        else:
            # Неположительный хвост только мешает — отрезаем его.
            ending_here = nums[index]
            start = index
        if ending_here > best:
            best, best_start, best_end = ending_here, start, index
    return best, best_start, best_end

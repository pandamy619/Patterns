"""Поиск числа в отсортированном массиве без повторов, сдвинутом по кругу.

Приём: exact match (поиск точного совпадения) + выбор отсортированной половины.
Аналог: LeetCode 33.
"""


def find_the_target_in_a_rotated_sorted_array(nums: list[int], target: int) -> int:
    """Индекс target или -1.

    Время O(log n), память O(1).
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Точка разрыва одна, поэтому хотя бы одна из половин отсортирована
        # «честно». Только про неё мы умеем за O(1) сказать, лежит ли там target.
        if nums[lo] <= nums[mid]:
            # Левая половина [lo, mid] без разрыва. Знак <= важен: при lo == mid
            # половина состоит из одного элемента и тоже считается отсортированной.
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # Иначе без разрыва правая половина [mid, hi].
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

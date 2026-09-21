"""Первое и последнее вхождение числа в отсортированный массив с повторами.

Приём: lower bound (нижняя граница) для первого вхождения и
upper bound (верхняя граница) для последнего — два независимых поиска.
Аналог: LeetCode 34.
"""


def first_and_last_occurrences_of_a_number(nums: list[int], target: int) -> list[int]:
    """[first, last] для target либо [-1, -1], если его нет.

    Время O(log n), память O(1).
    """
    first = _first_at_least(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    # target точно есть, так что второй поиск вернёт настоящий индекс.
    return [first, _last_at_most(nums, target)]


def _first_at_least(nums: list[int], target: int) -> int:
    """Первый индекс с nums[i] >= target или len(nums), если такого нет."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2          # сужаемся через hi = mid → округляем вниз
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _last_at_most(nums: list[int], target: int) -> int:
    """Последний индекс с nums[i] <= target или -1, если такого нет."""
    # lo = -1 — зеркальный «сторож»: он означает «подходящих элементов нет»
    # и никогда не читается из массива, потому что mid > lo.
    lo, hi = -1, len(nums) - 1
    while lo < hi:
        # Сужаемся через lo = mid, поэтому округляем ВВЕРХ. С округлением
        # вниз на диапазоне из двух элементов mid == lo, и цикл зависнет.
        mid = (lo + hi + 1) // 2
        if nums[mid] <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo

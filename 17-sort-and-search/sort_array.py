"""Отсортировать массив целых чисел по возрастанию.

Основной приём: quicksort (быстрая сортировка) со случайным опорным элементом
и разбиением на три зоны — «меньше», «равно», «больше».
Дополнительно: counting sort (сортировка подсчётом) для случая, когда значения
лежат в узком диапазоне.
Встроенные sorted / list.sort в решениях намеренно не используются.
Аналог: LeetCode 912.
"""

from __future__ import annotations

import random


def sort_array(nums: list[int]) -> list[int]:
    """Отсортировать nums на месте быстрой сортировкой и вернуть его же.

    Время O(n log n) в среднем, O(n²) в худшем — но при случайном опорном
    элементе худший случай зависит от везения, а не от входных данных.
    Память O(log n) — стек рекурсии. Сортировка нестабильна.
    """
    _quicksort(nums, 0, len(nums) - 1)
    return nums


def partition_three_way(nums: list[int], lo: int, hi: int, pivot: int) -> tuple[int, int]:
    """Переставить nums[lo..hi] так, чтобы слева оказались элементы меньше pivot,
    посередине — равные ему, справа — большие. Вернуть границы средней зоны (lt, gt):

        nums[lo..lt-1] < pivot,   nums[lt..gt] == pivot,   nums[gt+1..hi] > pivot

    Время O(hi - lo + 1), память O(1).
    """
    lt, i, gt = lo, lo, hi
    # Инвариант: [lo, lt) меньше pivot, [lt, i) равны ему, (gt, hi] больше,
    # а отрезок [i, gt] ещё не просмотрен. Каждый шаг сужает его на один элемент.
    while i <= gt:
        if nums[i] < pivot:
            nums[lt], nums[i] = nums[i], nums[lt]
            lt += 1
            i += 1
        elif nums[i] > pivot:
            nums[i], nums[gt] = nums[gt], nums[i]
            gt -= 1
            # i стоит на месте: из правой части приехал элемент, которого мы ещё не видели.
        else:
            i += 1
    return lt, gt


def _quicksort(nums: list[int], lo: int, hi: int) -> None:
    while lo < hi:
        # Опорный элемент — со случайной позиции. Любое фиксированное правило
        # («первый», «последний», «средний») можно сломать специально подобранным
        # входом, а «последний» ломается даже обычным отсортированным массивом.
        pivot = nums[random.randint(lo, hi)]
        lt, gt = partition_three_way(nums, lo, hi, pivot)
        # Зона «равно» уже на своём месте; остаются две части. В рекурсию уходим
        # только в меньшую, большую обрабатываем этим же циклом — так глубина
        # стека не превышает log n даже при самых неудачных опорных элементах.
        if lt - lo < hi - gt:
            _quicksort(nums, lo, lt - 1)
            lo = gt + 1
        else:
            _quicksort(nums, gt + 1, hi)
            hi = lt - 1


def sort_array_counting(nums: list[int]) -> list[int]:
    """Вернуть отсортированную копию nums, не сравнивая элементы между собой.

    Время O(n + r), память O(n + r), где r = max - min + 1 — ширина диапазона значений.
    Выгодно, когда r сравнимо с n или меньше; при r порядка 10⁹ не годится.
    """
    if not nums:
        return []

    smallest = min(nums)
    largest = max(nums)
    # Сдвиг на smallest превращает значения в индексы 0..r-1;
    # заодно бесплатно поддерживаются отрицательные числа.
    counts = [0] * (largest - smallest + 1)
    for value in nums:
        counts[value - smallest] += 1

    result: list[int] = []
    for offset, count in enumerate(counts):
        result.extend([smallest + offset] * count)
    return result

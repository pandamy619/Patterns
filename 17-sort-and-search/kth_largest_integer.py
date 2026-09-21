"""Найти k-й по величине элемент массива (k = 1 — максимум).

Основной приём: quickselect (быстрый выбор) — то же разбиение, что в quicksort,
но после него мы идём только в ту часть, где лежит нужная позиция.
Рядом — вариант с min-кучей размера k: он медленнее на готовом массиве,
зато годится для потока данных.
Аналог: LeetCode 215.
"""

from __future__ import annotations

import heapq
import random

from sort_array import partition_three_way


def kth_largest_integer(nums: list[int], k: int) -> int:
    """Вернуть k-й по величине элемент (дубликаты считаются отдельными элементами).

    Время O(n) в среднем, O(n²) в худшем (при случайном опорном элементе
    практически недостижим). Память O(n) — только на копию, чтобы не портить
    массив вызывающему; если вход можно менять, копия не нужна и память O(1).
    """
    _check_k(nums, k)
    work = list(nums)
    # k-й по величине — это элемент, который в отсортированном по возрастанию
    # массиве стоял бы на позиции n - k. Дальше ищем «кто стоит на этой позиции».
    target = len(work) - k
    lo, hi = 0, len(work) - 1
    while True:
        pivot = work[random.randint(lo, hi)]
        lt, gt = partition_three_way(work, lo, hi, pivot)
        # После разбиения зона [lt..gt] занимает свои окончательные позиции.
        if target < lt:
            hi = lt - 1        # нужная позиция среди меньших — правую часть выбрасываем
        elif target > gt:
            lo = gt + 1        # нужная позиция среди больших — выбрасываем левую
        else:
            return pivot       # попали в зону «равно» — её значение и есть ответ


def kth_largest_integer_heap(nums: list[int], k: int) -> int:
    """То же самое через min-кучу, в которой живут k самых больших из просмотренных.

    Время O(n log k), память O(k).
    """
    _check_k(nums, k)
    top: list[int] = []
    for value in nums:
        if len(top) < k:
            heapq.heappush(top, value)
        elif value > top[0]:
            # Новый элемент вытесняет самого слабого из топ-k;
            # heapreplace делает «извлечь + вставить» за одно просеивание.
            heapq.heapreplace(top, value)
    # В куче k наибольших, на вершине — наименьший из них, то есть k-й по величине.
    return top[0]


def _check_k(nums: list[int], k: int) -> None:
    if not 1 <= k <= len(nums):
        raise ValueError(f"k должно быть от 1 до {len(nums)}, получено {k}")

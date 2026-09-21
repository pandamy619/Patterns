"""Тесты к паттерну Intervals.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор медленный, зато очевидно правильный.

Соглашение о концах: в первых двух задачах интервалы закрытые, [start, end],
в третьей — полуоткрытые, [start, end). Тесты фиксируют это явно.
"""

import random

from identify_all_interval_overlaps import identify_all_interval_overlaps
from largest_overlap_of_intervals import (
    largest_overlap_of_intervals,
    largest_overlap_two_arrays,
)
from merge_overlapping_intervals import merge_overlapping_intervals

RNG = random.Random(2024)
ROUNDS = 500


def _random_intervals(max_count, max_point, min_length=0):
    """Случайные интервалы в произвольном порядке, возможны дубликаты."""
    result = []
    for _ in range(RNG.randint(0, max_count)):
        start = RNG.randint(0, max_point - min_length)
        result.append([start, RNG.randint(start + min_length, max_point)])
    return result


def _random_disjoint_sorted(max_point):
    """Отсортированный список закрытых интервалов без общих точек."""
    result = []
    point = RNG.randint(0, 3)
    while point < max_point:
        end = min(max_point, point + RNG.randint(1, 4))
        result.append([point, end])
        # +1 как минимум: закрытые соседи не должны даже касаться.
        point = end + RNG.randint(1, 4)
    return result


# ---------- merge_overlapping_intervals ----------

def _merge_brute(intervals):
    """Закрашиваем точки на удвоенной оси и читаем сплошные полосы.

    Удвоение нужно, чтобы отличить [1, 2] + [3, 4] (между ними дырка 2.5)
    от [1, 2] + [2, 3] (дырки нет).
    """
    painted = set()
    for start, end in intervals:
        painted.update(range(2 * start, 2 * end + 1))
    result = []
    for point in sorted(painted):
        if point - 1 not in painted:
            result.append([point // 2, None])
        if point + 1 not in painted:
            result[-1][1] = point // 2
    return result


def test_merge_overlapping_intervals_examples():
    assert merge_overlapping_intervals(
        [[8, 10], [1, 3], [15, 16], [2, 6], [9, 12], [4, 5]]
    ) == [[1, 6], [8, 12], [15, 16]]
    assert merge_overlapping_intervals([[5, 9]]) == [[5, 9]]
    assert merge_overlapping_intervals([]) == []
    assert merge_overlapping_intervals([[2, 3], [2, 3]]) == [[2, 3]]
    assert merge_overlapping_intervals([[-5, -2], [-3, 0]]) == [[-5, 0]]


def test_merge_overlapping_intervals_closed_ends():
    # Общая точка — уже пересечение.
    assert merge_overlapping_intervals([[1, 4], [4, 6]]) == [[1, 6]]
    # Соседние целые точки общей точки не дают.
    assert merge_overlapping_intervals([[1, 4], [5, 6]]) == [[1, 4], [5, 6]]
    # Интервал-точка приклеивается к краю.
    assert merge_overlapping_intervals([[3, 3], [1, 3]]) == [[1, 3]]


def test_merge_overlapping_intervals_nested():
    # Вложенный интервал не должен укоротить внешний.
    assert merge_overlapping_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]
    assert merge_overlapping_intervals([[2, 3], [1, 10], [9, 12]]) == [[1, 12]]


def test_merge_overlapping_intervals_does_not_mutate_input():
    intervals = [[4, 7], [1, 5]]
    merge_overlapping_intervals(intervals)
    assert intervals == [[4, 7], [1, 5]]


def test_merge_overlapping_intervals_random():
    for _ in range(ROUNDS):
        intervals = _random_intervals(max_count=8, max_point=15)
        assert merge_overlapping_intervals(intervals) == _merge_brute(intervals)


# ---------- identify_all_interval_overlaps ----------

def _overlaps_brute(first, second):
    result = []
    for a_start, a_end in first:
        for b_start, b_end in second:
            lo, hi = max(a_start, b_start), min(a_end, b_end)
            if lo <= hi:
                result.append([lo, hi])
    return sorted(result)


def test_identify_all_interval_overlaps_examples():
    assert identify_all_interval_overlaps(
        [[0, 3], [6, 8], [11, 15]],
        [[2, 7], [8, 9], [12, 13], [14, 20]],
    ) == [[2, 3], [6, 7], [8, 8], [12, 13], [14, 15]]
    assert identify_all_interval_overlaps([[1, 2], [7, 9]], [[3, 6]]) == []
    assert identify_all_interval_overlaps([], [[1, 2]]) == []
    assert identify_all_interval_overlaps([[1, 2]], []) == []
    assert identify_all_interval_overlaps([], []) == []


def test_identify_all_interval_overlaps_closed_ends():
    # Касание в одной точке — пересечение нулевой длины.
    assert identify_all_interval_overlaps([[1, 4]], [[4, 9]]) == [[4, 4]]
    assert identify_all_interval_overlaps([[1, 4]], [[5, 9]]) == []
    # Один длинный интервал задевает нескольких соседей, в том числе краями.
    assert identify_all_interval_overlaps(
        [[2, 10]], [[0, 2], [4, 5], [10, 12]]
    ) == [[2, 2], [4, 5], [10, 10]]


def test_identify_all_interval_overlaps_equal_ends():
    # Концы совпали: неважно, какой указатель сдвинуть, ничего не теряется.
    assert identify_all_interval_overlaps(
        [[1, 5], [6, 9]], [[3, 5], [7, 8]]
    ) == [[3, 5], [7, 8]]
    assert identify_all_interval_overlaps([[1, 5]], [[1, 5]]) == [[1, 5]]


def test_identify_all_interval_overlaps_random():
    for _ in range(ROUNDS):
        first = _random_disjoint_sorted(max_point=25)
        second = _random_disjoint_sorted(max_point=25)
        expected = _overlaps_brute(first, second)
        assert identify_all_interval_overlaps(first, second) == expected
        # Операция симметрична.
        assert identify_all_interval_overlaps(second, first) == expected


# ---------- largest_overlap_of_intervals ----------

BOTH_VARIANTS = (largest_overlap_of_intervals, largest_overlap_two_arrays)


def _largest_overlap_brute(intervals):
    """Максимум всегда достигается в чьём-то начале: между началами счётчик
    активных может только убывать. Считаем активных в каждой такой точке."""
    return max(
        (sum(1 for start, end in intervals if start <= point < end)
         for point, _ in intervals),
        default=0,
    )


def test_largest_overlap_of_intervals_examples():
    for solve in BOTH_VARIANTS:
        assert solve([[1, 5], [2, 4], [4, 9], [3, 7], [7, 8]]) == 3
        assert solve([[2, 6]]) == 1
        assert solve([]) == 0
        assert solve([[1, 2], [5, 6], [9, 10]]) == 1
        assert solve([[3, 8], [3, 8], [3, 8]]) == 3
        assert solve([[-4, 0], [-2, 3]]) == 2


def test_largest_overlap_of_intervals_half_open_ends():
    for solve in BOTH_VARIANTS:
        # Конец не входит: в точке 3 первый интервал уже закончился.
        assert solve([[1, 3], [3, 5]]) == 1
        assert solve([[1, 3], [3, 5], [3, 4], [0, 3]]) == 2
        # А начало входит: одинаковые начала считаются вместе.
        assert solve([[3, 5], [3, 4]]) == 2
        # Стоит сдвинуть конец на единицу — и пересечение появляется.
        assert solve([[1, 4], [3, 5]]) == 2


def test_largest_overlap_of_intervals_nested():
    for solve in BOTH_VARIANTS:
        assert solve([[0, 10], [1, 9], [2, 8], [3, 7]]) == 4


def test_largest_overlap_of_intervals_random():
    for _ in range(ROUNDS):
        intervals = _random_intervals(max_count=9, max_point=12, min_length=1)
        expected = _largest_overlap_brute(intervals)
        for solve in BOTH_VARIANTS:
            assert solve(intervals) == expected


def test_largest_overlap_of_intervals_does_not_mutate_input():
    intervals = [[5, 9], [1, 6]]
    for solve in BOTH_VARIANTS:
        solve(intervals)
        assert intervals == [[5, 9], [1, 6]]

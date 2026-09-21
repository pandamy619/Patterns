"""Тесты к паттерну Binary Search.

Кроме ручных примеров каждое решение сверяется с линейным перебором
на случайных данных: перебор медленный, зато очевидно правильный.
Маленькие массивы (0–3 элемента) генерируются намеренно часто — именно
на них бинарный поиск зацикливается или промахивается на единицу.
"""

import random
from collections import Counter

import pytest

from cutting_wood import cutting_wood
from find_the_insertion_index import find_the_insertion_index
from find_the_target_in_a_rotated_sorted_array import (
    find_the_target_in_a_rotated_sorted_array,
)
from first_and_last_occurrences_of_a_number import (
    first_and_last_occurrences_of_a_number,
)
from local_maxima_in_array import local_maxima_in_array
from matrix_search import matrix_search
from weighted_random_selection import WeightedRandomSelection

RNG = random.Random(2024)
ROUNDS = 500


def _sorted_unique(max_len: int) -> list[int]:
    return sorted(RNG.sample(range(-20, 21), RNG.randint(0, max_len)))


# ---------- find_the_insertion_index ----------

def test_find_the_insertion_index_examples():
    nums = [-4, 0, 3, 8, 15]
    assert find_the_insertion_index(nums, 8) == 3       # число есть
    assert find_the_insertion_index(nums, 5) == 3       # между 3 и 8
    assert find_the_insertion_index(nums, -9) == 0      # левее всех
    assert find_the_insertion_index(nums, 99) == 5      # правее всех: индекс == len
    assert find_the_insertion_index(nums, -4) == 0
    assert find_the_insertion_index(nums, 15) == 4
    assert find_the_insertion_index([], 7) == 0
    assert find_the_insertion_index([7], 7) == 0
    assert find_the_insertion_index([7], 8) == 1


def test_find_the_insertion_index_random():
    for _ in range(ROUNDS):
        nums = _sorted_unique(10)
        target = RNG.randint(-22, 22)
        expected = sum(1 for value in nums if value < target)
        assert find_the_insertion_index(nums, target) == expected


# ---------- first_and_last_occurrences_of_a_number ----------

def _first_last_brute(nums, target):
    hits = [i for i, value in enumerate(nums) if value == target]
    return [hits[0], hits[-1]] if hits else [-1, -1]


def test_first_and_last_occurrences_examples():
    nums = [2, 5, 5, 5, 9, 9, 14]
    assert first_and_last_occurrences_of_a_number(nums, 5) == [1, 3]
    assert first_and_last_occurrences_of_a_number(nums, 9) == [4, 5]
    assert first_and_last_occurrences_of_a_number(nums, 2) == [0, 0]     # левый край
    assert first_and_last_occurrences_of_a_number(nums, 14) == [6, 6]    # правый край
    assert first_and_last_occurrences_of_a_number(nums, 7) == [-1, -1]   # «дырка» внутри
    assert first_and_last_occurrences_of_a_number(nums, 1) == [-1, -1]   # меньше всех
    assert first_and_last_occurrences_of_a_number(nums, 20) == [-1, -1]  # больше всех
    assert first_and_last_occurrences_of_a_number([4, 4, 4, 4], 4) == [0, 3]
    assert first_and_last_occurrences_of_a_number([4], 4) == [0, 0]
    assert first_and_last_occurrences_of_a_number([], 4) == [-1, -1]


def test_first_and_last_occurrences_random():
    for _ in range(ROUNDS):
        nums = sorted(RNG.randint(0, 6) for _ in range(RNG.randint(0, 12)))
        target = RNG.randint(-1, 7)
        assert first_and_last_occurrences_of_a_number(nums, target) == _first_last_brute(
            nums, target
        )


# ---------- cutting_wood ----------

def _cutting_wood_brute(heights, k):
    for saw in range(max(heights, default=0), -1, -1):
        if sum(max(0, tree - saw) for tree in heights) >= k:
            return saw
    return -1


def test_cutting_wood_examples():
    assert cutting_wood([7, 2, 10, 5], 8) == 4
    assert cutting_wood([7, 2, 10, 5], 11) == 3      # при H=4 срезали бы только 10 — мало
    assert cutting_wood([7, 2, 10, 5], 1) == 9       # хватит верхушки самого высокого
    assert cutting_wood([7, 2, 10, 5], 24) == 0      # приходится пилить под корень
    assert cutting_wood([7, 2, 10, 5], 25) == -1     # столько древесины просто нет
    assert cutting_wood([7, 2, 10, 5], 0) == 10      # ничего не нужно — пила на максимуме
    assert cutting_wood([6], 6) == 0
    assert cutting_wood([6], 2) == 4
    assert cutting_wood([5, 5, 5], 3) == 4
    assert cutting_wood([], 1) == -1


def test_cutting_wood_random():
    for _ in range(ROUNDS):
        heights = [RNG.randint(0, 15) for _ in range(RNG.randint(0, 7))]
        k = RNG.randint(0, 40)
        assert cutting_wood(heights, k) == _cutting_wood_brute(heights, k)


def test_cutting_wood_is_logarithmic_in_height():
    # Перебор всех высот здесь потребовал бы миллиард шагов.
    assert cutting_wood([10**9, 10**9], 2) == 10**9 - 1


# ---------- find_the_target_in_a_rotated_sorted_array ----------

def test_rotated_array_examples():
    nums = [11, 14, 20, 1, 4, 6, 9]
    for index, value in enumerate(nums):
        assert find_the_target_in_a_rotated_sorted_array(nums, value) == index
    assert find_the_target_in_a_rotated_sorted_array(nums, 5) == -1
    assert find_the_target_in_a_rotated_sorted_array(nums, 0) == -1
    assert find_the_target_in_a_rotated_sorted_array(nums, 25) == -1
    assert find_the_target_in_a_rotated_sorted_array([1, 2, 3, 4], 3) == 2   # сдвига нет
    assert find_the_target_in_a_rotated_sorted_array([2, 1], 1) == 1         # lo == mid
    assert find_the_target_in_a_rotated_sorted_array([2, 1], 2) == 0
    assert find_the_target_in_a_rotated_sorted_array([5], 5) == 0
    assert find_the_target_in_a_rotated_sorted_array([5], 6) == -1
    assert find_the_target_in_a_rotated_sorted_array([], 6) == -1


def test_rotated_array_random():
    for _ in range(ROUNDS):
        base = _sorted_unique(10)
        shift = RNG.randint(0, len(base)) if base else 0
        nums = base[shift:] + base[:shift]
        target = RNG.randint(-22, 22)
        expected = nums.index(target) if target in nums else -1
        assert find_the_target_in_a_rotated_sorted_array(nums, target) == expected


# ---------- local_maxima_in_array ----------

def _is_local_maximum(nums, index):
    left_ok = index == 0 or nums[index - 1] < nums[index]
    right_ok = index == len(nums) - 1 or nums[index] > nums[index + 1]
    return left_ok and right_ok


def test_local_maxima_examples():
    assert local_maxima_in_array([3, 8, 12, 7, 9, 4, 1]) in (2, 4)
    assert local_maxima_in_array([1, 2, 3, 4]) == 3      # сплошной подъём — вершина на краю
    assert local_maxima_in_array([9, 6, 2]) == 0         # сплошной спуск
    assert local_maxima_in_array([1, 5, 1]) == 1
    assert local_maxima_in_array([5, 1, 5]) in (0, 2)
    assert local_maxima_in_array([42]) == 0
    assert local_maxima_in_array([-3, -1]) == 1


def test_local_maxima_rejects_empty():
    with pytest.raises(ValueError):
        local_maxima_in_array([])


def test_local_maxima_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-9, 9)]
        for _ in range(RNG.randint(0, 11)):
            step = RNG.choice([-3, -2, -1, 1, 2, 3])     # соседи всегда различны
            nums.append(nums[-1] + step)
        index = local_maxima_in_array(nums)
        assert 0 <= index < len(nums)
        assert _is_local_maximum(nums, index)


# ---------- weighted_random_selection ----------

class _ScriptedRandom:
    """Подмена генератора: выдаёт заранее заданные числа и проверяет границы."""

    def __init__(self, script):
        self._script = list(script)
        self.calls = []

    def randint(self, a, b):
        self.calls.append((a, b))
        value = self._script.pop(0)
        assert a <= value <= b
        return value


def test_weighted_random_selection_deterministic():
    # Веса [3, 1, 4] режут отрезок 1..8 на куски: 1-3 → 0, 4 → 1, 5-8 → 2.
    expected = [0, 0, 0, 1, 2, 2, 2, 2]
    fake = _ScriptedRandom(range(1, 9))
    selector = WeightedRandomSelection([3, 1, 4], rng=fake)
    assert [selector.pick() for _ in range(8)] == expected
    assert fake.calls == [(1, 8)] * 8


def test_weighted_random_selection_every_dart_matches_brute():
    # Перебираем ВСЕ возможные значения «дротика» и сверяем с линейным поиском.
    for _ in range(ROUNDS):
        weights = [RNG.randint(0, 4) for _ in range(RNG.randint(1, 7))]
        if sum(weights) == 0:
            weights[RNG.randrange(len(weights))] = 1
        total = sum(weights)
        selector = WeightedRandomSelection(weights, rng=_ScriptedRandom(range(1, total + 1)))
        picks = [selector.pick() for _ in range(total)]

        brute = [index for index, weight in enumerate(weights) for _ in range(weight)]
        assert picks == brute
        # Прямое следствие: каждый индекс выпадает ровно weights[i] раз из total.
        assert Counter(picks) == Counter({i: w for i, w in enumerate(weights) if w})


def test_weighted_random_selection_statistics():
    weights = [1, 0, 6, 3]
    draws = 60_000
    selector = WeightedRandomSelection(weights, rng=random.Random(2024))
    counts = Counter(selector.pick() for _ in range(draws))

    assert counts[1] == 0                                 # нулевой вес не выпадает никогда
    for index, weight in enumerate(weights):
        share = counts[index] / draws
        assert share == pytest.approx(weight / sum(weights), abs=0.01)


def test_weighted_random_selection_single_and_default_rng():
    selector = WeightedRandomSelection([5])               # генератор по умолчанию
    assert {selector.pick() for _ in range(20)} == {0}


def test_weighted_random_selection_rejects_bad_weights():
    for bad in ([], [0, 0], [2, -1, 3]):
        with pytest.raises(ValueError):
            WeightedRandomSelection(bad)


# ---------- matrix_search ----------

def test_matrix_search_examples():
    matrix = [
        [1, 4, 6],
        [9, 13, 17],
        [20, 28, 35],
    ]
    for row in matrix:
        for value in row:
            assert matrix_search(matrix, value)
    for missing in (0, 5, 8, 18, 19, 40):                 # в т. ч. «между строками»
        assert not matrix_search(matrix, missing)

    assert matrix_search([[3, 7, 8]], 7)                  # одна строка
    assert matrix_search([[3], [7], [8]], 8)              # один столбец
    assert not matrix_search([[3], [7], [8]], 5)
    assert matrix_search([[3]], 3)
    assert not matrix_search([[3]], 4)
    assert not matrix_search([], 1)
    assert not matrix_search([[]], 1)


def test_matrix_search_random():
    for _ in range(ROUNDS):
        rows, cols = RNG.randint(1, 5), RNG.randint(1, 5)
        flat = sorted(RNG.sample(range(-30, 31), rows * cols))
        matrix = [flat[r * cols:(r + 1) * cols] for r in range(rows)]
        target = RNG.randint(-32, 32)
        assert matrix_search(matrix, target) == (target in flat)

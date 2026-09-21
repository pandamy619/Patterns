"""Тесты к паттерну Prefix Sums.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор медленный, зато очевидно правильный.
"""

import random
from math import prod

import pytest

from k_sum_subarrays import k_sum_subarrays, k_sum_subarrays_quadratic
from product_array_without_current_element import (
    product_array_with_division,
    product_array_without_current_element,
)
from sum_between_range import SumBetweenRange

RNG = random.Random(2024)
ROUNDS = 500


# ---------- sum_between_range ----------

def test_sum_between_range_examples():
    ranges = SumBetweenRange([4, -2, 7, 1, -5, 3])
    assert ranges.sum_range(1, 3) == 6
    assert ranges.sum_range(0, 5) == 8       # весь массив
    assert ranges.sum_range(0, 0) == 4       # отрезок от самого начала
    assert ranges.sum_range(4, 4) == -5      # один элемент
    assert ranges.sum_range(3, 5) == -1      # до самого конца

    single = SumBetweenRange([-9])
    assert single.sum_range(0, 0) == -9


def test_sum_between_range_rejects_bad_ranges():
    ranges = SumBetweenRange([4, -2, 7])
    for i, j in [(2, 1), (-1, 1), (0, 3), (3, 3), (-3, -1)]:
        with pytest.raises(IndexError):
            ranges.sum_range(i, j)
    with pytest.raises(IndexError):
        SumBetweenRange([]).sum_range(0, 0)


def test_sum_between_range_keeps_input_intact():
    nums = [5, 1, -4]
    ranges = SumBetweenRange(nums)
    assert nums == [5, 1, -4]
    # Структура рассчитана на неизменяемый массив: более поздние правки
    # исходного списка на ответы не влияют.
    nums[0] = 100
    assert ranges.sum_range(0, 2) == 2


def test_sum_between_range_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-20, 20) for _ in range(RNG.randint(1, 12))]
        ranges = SumBetweenRange(nums)
        for _ in range(10):
            i = RNG.randrange(len(nums))
            j = RNG.randrange(i, len(nums))
            assert ranges.sum_range(i, j) == sum(nums[i:j + 1])


# ---------- k_sum_subarrays ----------

def _k_sum_brute(nums, k):
    return sum(
        1
        for start in range(len(nums))
        for end in range(start, len(nums))
        if sum(nums[start:end + 1]) == k
    )


@pytest.mark.parametrize("solve", [k_sum_subarrays, k_sum_subarrays_quadratic])
def test_k_sum_subarrays_examples(solve):
    assert solve([2, 1, -1, 3, -2, 2], 3) == 6
    assert solve([4, -1], 3) == 1               # тут окно с двумя указателями ошибается
    assert solve([5], 5) == 1                   # без пустого префикса было бы 0
    assert solve([5], 0) == 0                   # пустой подмассив не считается
    assert solve([0, 0, 0], 0) == 6             # все 3·4/2 подмассива
    assert solve([1, -1, 1, -1], 0) == 4
    assert solve([-2, -3, -1], -5) == 1         # отрицательная цель
    assert solve([1, 2, 3], 100) == 0
    assert solve([], 0) == 0
    assert solve([], 7) == 0


@pytest.mark.parametrize("solve", [k_sum_subarrays, k_sum_subarrays_quadratic])
def test_k_sum_subarrays_random(solve):
    for _ in range(ROUNDS):
        nums = [RNG.randint(-5, 5) for _ in range(RNG.randint(0, 10))]
        k = RNG.randint(-8, 8)
        assert solve(nums, k) == _k_sum_brute(nums, k)


def test_k_sum_subarrays_is_linear_on_long_input():
    # Квадратичное решение сделало бы здесь 2·10^10 сравнений.
    size = 200_000
    assert k_sum_subarrays([0] * size, 0) == size * (size + 1) // 2


# ---------- product_array_without_current_element ----------

def _product_brute(nums):
    return [prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]


SOLVERS = [product_array_without_current_element, product_array_with_division]


@pytest.mark.parametrize("solve", SOLVERS)
def test_product_array_examples(solve):
    assert solve([3, 2, 5, 4]) == [40, 60, 24, 30]
    assert solve([-1, 2, -3]) == [-6, 3, -2]          # знаки
    assert solve([3, 0, 5, 4]) == [0, 60, 0, 0]       # один ноль
    assert solve([0, 2, 0]) == [0, 0, 0]              # два нуля
    assert solve([0, 7]) == [7, 0]
    assert solve([6, 9]) == [9, 6]
    assert solve([8]) == [1]                          # пустое произведение
    assert solve([0]) == [1]
    assert solve([]) == []


@pytest.mark.parametrize("solve", SOLVERS)
def test_product_array_does_not_modify_input(solve):
    nums = [3, 0, -2]
    solve(nums)
    assert nums == [3, 0, -2]


@pytest.mark.parametrize("solve", SOLVERS)
def test_product_array_random(solve):
    for _ in range(ROUNDS):
        # Нули выпадают часто — это самый коварный случай.
        nums = [RNG.choice([-3, -2, -1, 0, 0, 1, 2, 3, 4]) for _ in range(RNG.randint(0, 9))]
        assert solve(nums) == _product_brute(nums)

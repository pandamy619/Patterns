"""Тесты к паттерну Backtracking.

Кроме ручных примеров каждое решение сверяется с эталоном из itertools
на случайных данных: там перебор готовый и заведомо правильный.
"""

import random
from itertools import combinations, combinations_with_replacement, permutations, product
from math import factorial

import pytest

from combinations_of_a_sum import combinations_of_a_sum
from find_all_permutations import find_all_permutations
from find_all_subsets import find_all_subsets
from n_queens import n_queens
from phone_keypad_combinations import KEYPAD, phone_keypad_combinations

RNG = random.Random(2024)
ROUNDS = 300


def _distinct_numbers(max_size):
    return RNG.sample(range(-20, 21), RNG.randint(0, max_size))


# ---------- find_all_permutations ----------

def test_find_all_permutations_examples():
    assert find_all_permutations([5, 2, 8]) == [
        [5, 2, 8], [5, 8, 2], [2, 5, 8], [2, 8, 5], [8, 5, 2], [8, 2, 5],
    ]
    assert find_all_permutations([7]) == [[7]]
    assert find_all_permutations([]) == [[]]          # 0! = 1
    assert find_all_permutations([-1, 0]) == [[-1, 0], [0, -1]]


def test_find_all_permutations_does_not_touch_input():
    nums = [3, 1, 2]
    find_all_permutations(nums)
    assert nums == [3, 1, 2]


def test_find_all_permutations_returns_independent_lists():
    answer = find_all_permutations([1, 2, 3])
    answer[0].append(99)                              # порча одного списка...
    assert all(len(p) == 3 for p in answer[1:])       # ...не задевает остальные


def test_find_all_permutations_random():
    for _ in range(ROUNDS):
        nums = _distinct_numbers(6)
        answer = find_all_permutations(nums)
        assert len(answer) == factorial(len(nums))
        # Порядок обхода у нас тот же, что у itertools: по индексам слева направо.
        assert answer == [list(p) for p in permutations(nums)]


# ---------- find_all_subsets ----------

def _subsets_reference(nums):
    return sorted(
        list(c) for size in range(len(nums) + 1) for c in combinations(nums, size)
    )


def test_find_all_subsets_examples():
    assert find_all_subsets([4, 9]) == [[], [9], [4], [4, 9]]
    assert find_all_subsets([]) == [[]]
    assert find_all_subsets([0]) == [[], [0]]
    assert sorted(find_all_subsets([3, 1, 2])) == [
        [], [1], [1, 2], [2], [3], [3, 1], [3, 1, 2], [3, 2],
    ]


def test_find_all_subsets_returns_independent_lists():
    answer = find_all_subsets([1, 2, 3])
    answer[0].append(99)
    assert answer.count([99]) == 1 and [] not in answer[1:]


def test_find_all_subsets_random():
    for _ in range(ROUNDS):
        nums = _distinct_numbers(8)
        answer = find_all_subsets(nums)
        assert len(answer) == 2 ** len(nums)
        assert sorted(answer) == _subsets_reference(nums)


# ---------- n_queens ----------

def _n_queens_reference(n):
    # Перестановка столбцов уже гарантирует разные строки и столбцы,
    # остаётся проверить диагонали.
    return sum(
        1
        for cols in permutations(range(n))
        if len({r - c for r, c in enumerate(cols)}) == n
        and len({r + c for r, c in enumerate(cols)}) == n
    )


def test_n_queens_examples():
    assert n_queens(1) == 1
    assert n_queens(2) == 0
    assert n_queens(3) == 0
    assert n_queens(4) == 2
    assert n_queens(6) == 4           # меньше, чем для n = 5: монотонности нет
    assert n_queens(8) == 92
    assert n_queens(0) == 1           # пустая расстановка


def test_n_queens_rejects_negative():
    with pytest.raises(ValueError):
        n_queens(-1)


@pytest.mark.parametrize("n", range(9))
def test_n_queens_matches_reference(n):
    assert n_queens(n) == _n_queens_reference(n)


def test_n_queens_is_fast_enough():
    # Полный перебор 10! перестановок с проверкой занял бы секунды,
    # с отсечениями — доли секунды.
    assert n_queens(10) == 724


# ---------- combinations_of_a_sum ----------

def _combinations_reference(nums, target):
    if target < 0:
        return []
    if not nums:
        return [[]] if target == 0 else []
    longest = target // min(nums)
    return sorted(
        list(c)
        for size in range(longest + 1)
        for c in combinations_with_replacement(sorted(nums), size)
        if sum(c) == target
    )


def test_combinations_of_a_sum_examples():
    assert combinations_of_a_sum([2, 3, 5], 9) == [
        [2, 2, 2, 3], [2, 2, 5], [3, 3, 3],
    ]
    assert combinations_of_a_sum([5, 3, 2], 9) == [   # порядок входа не важен
        [2, 2, 2, 3], [2, 2, 5], [3, 3, 3],
    ]
    assert combinations_of_a_sum([4, 6], 9) == []     # из чётных нечётное не собрать
    assert combinations_of_a_sum([7], 7) == [[7]]
    assert combinations_of_a_sum([7], 21) == [[7, 7, 7]]
    assert combinations_of_a_sum([10], 3) == []
    assert combinations_of_a_sum([], 5) == []
    assert combinations_of_a_sum([1, 2], 0) == [[]]
    assert combinations_of_a_sum([1, 2], -3) == []


def test_combinations_of_a_sum_rejects_non_positive():
    with pytest.raises(ValueError):
        combinations_of_a_sum([0, 1], 3)
    with pytest.raises(ValueError):
        combinations_of_a_sum([-2, 5], 3)


def test_combinations_of_a_sum_random():
    for _ in range(ROUNDS):
        nums = RNG.sample(range(1, 10), RNG.randint(0, 5))
        target = RNG.randint(0, 14)
        answer = combinations_of_a_sum(nums, target)
        assert all(combo == sorted(combo) for combo in answer)
        assert sorted(answer) == _combinations_reference(nums, target)


# ---------- phone_keypad_combinations ----------

def test_phone_keypad_combinations_examples():
    assert phone_keypad_combinations("47") == [
        "gp", "gq", "gr", "gs", "hp", "hq", "hr", "hs", "ip", "iq", "ir", "is",
    ]
    assert phone_keypad_combinations("9") == ["w", "x", "y", "z"]
    assert phone_keypad_combinations("") == []
    assert len(phone_keypad_combinations("7979")) == 4 ** 4
    assert phone_keypad_combinations("22") == [
        "aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc",
    ]


@pytest.mark.parametrize("bad", ["1", "20", "5a", "3 4", "#"])
def test_phone_keypad_combinations_rejects_keys_without_letters(bad):
    with pytest.raises(ValueError):
        phone_keypad_combinations(bad)


def test_phone_keypad_combinations_random():
    for _ in range(ROUNDS):
        digits = "".join(RNG.choice("23456789") for _ in range(RNG.randint(1, 5)))
        expected = ["".join(p) for p in product(*(KEYPAD[d] for d in digits))]
        assert phone_keypad_combinations(digits) == expected

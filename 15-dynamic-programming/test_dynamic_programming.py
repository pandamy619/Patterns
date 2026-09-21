"""Тесты к паттерну Dynamic Programming.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор экспоненциальный, зато очевидно правильный.
Разные варианты одной задачи (top-down, таблица, сжатая память) прогоняются
через одни и те же проверки.
"""

import random
from itertools import combinations, product

import pytest

from climbing_stairs import (
    climbing_stairs,
    climbing_stairs_memo,
    climbing_stairs_recursive,
    climbing_stairs_table,
)
from longest_common_subsequence import (
    longest_common_subsequence,
    longest_common_subsequence_two_rows,
    restore_common_subsequence,
)
from longest_palindrome_in_a_string import (
    longest_palindrome_in_a_string,
    longest_palindrome_in_a_string_table,
)
from matrix_pathways import matrix_pathways, matrix_pathways_formula, matrix_pathways_grid
from maximum_subarray_sum import maximum_subarray_sum, maximum_subarray_with_bounds
from minimum_coin_combination import minimum_coin_combination, minimum_coin_combination_memo
from neighborhood_burglary import neighborhood_burglary, neighborhood_burglary_table
from zero_one_knapsack import (
    zero_one_knapsack,
    zero_one_knapsack_items,
    zero_one_knapsack_table,
)

RNG = random.Random(2024)
ROUNDS = 300


# ---------- climbing_stairs ----------

STAIRS = [climbing_stairs_recursive, climbing_stairs_memo, climbing_stairs_table, climbing_stairs]


def _stairs_brute(steps):
    """Честно перечисляем все последовательности из единиц и двоек."""
    total = 0
    for length in range(steps + 1):
        total += sum(1 for moves in product((1, 2), repeat=length) if sum(moves) == steps)
    return total


@pytest.mark.parametrize("solve", STAIRS)
def test_climbing_stairs_examples(solve):
    assert solve(0) == 1            # единственный способ — никуда не идти
    assert solve(1) == 1
    assert solve(2) == 2
    assert solve(3) == 3
    assert solve(6) == 13
    with pytest.raises(ValueError):
        solve(-1)


@pytest.mark.parametrize("solve", STAIRS)
def test_climbing_stairs_brute(solve):
    for steps in range(13):
        assert solve(steps) == _stairs_brute(steps)


def test_climbing_stairs_large():
    # Наивная рекурсия тут не дожила бы до ответа.
    assert climbing_stairs(90) == climbing_stairs_table(90) == climbing_stairs_memo(90)
    assert climbing_stairs(90) == 4660046610375530309


# ---------- minimum_coin_combination ----------

COINS = [minimum_coin_combination, minimum_coin_combination_memo]


def _coins_brute(coins, target):
    """Поиск в ширину по суммам: первый раз попали в target — это и есть минимум."""
    frontier, seen, used = {0}, {0}, 0
    while frontier:
        if target in frontier:
            return used
        frontier = {s + c for s in frontier for c in coins if s + c <= target} - seen
        seen |= frontier
        used += 1
    return -1


@pytest.mark.parametrize("solve", COINS)
def test_minimum_coin_combination_examples(solve):
    assert solve([1, 4, 6], 8) == 2             # 4 + 4; жадное 6 + 1 + 1 хуже
    assert solve([5, 7], 24) == 4               # 5 + 5 + 7 + 7
    assert solve([4, 6], 9) == -1               # чётными монетами нечётное не набрать
    assert solve([3], 2) == -1
    assert solve([3, 8], 0) == 0                # ноль набирается нулём монет
    assert solve([], 0) == 0
    assert solve([], 5) == -1
    assert solve([2, 2, 5], 9) == 3             # повторы номиналов не мешают


@pytest.mark.parametrize("solve", COINS)
def test_minimum_coin_combination_rejects_bad_input(solve):
    with pytest.raises(ValueError):
        solve([1, 0], 3)
    with pytest.raises(ValueError):
        solve([1], -1)


@pytest.mark.parametrize("solve", COINS)
def test_minimum_coin_combination_random(solve):
    for _ in range(ROUNDS):
        coins = [RNG.randint(1, 9) for _ in range(RNG.randint(0, 4))]
        target = RNG.randint(0, 30)
        assert solve(coins, target) == _coins_brute(coins, target)


# ---------- matrix_pathways ----------

PATHS = [matrix_pathways_grid, matrix_pathways, matrix_pathways_formula]


def _paths_brute(rows, cols):
    """Обход всех маршрутов без запоминания."""
    def walk(r, c):
        if r == rows - 1 and c == cols - 1:
            return 1
        total = 0
        if r + 1 < rows:
            total += walk(r + 1, c)
        if c + 1 < cols:
            total += walk(r, c + 1)
        return total

    return walk(0, 0)


@pytest.mark.parametrize("solve", PATHS)
def test_matrix_pathways_examples(solve):
    assert solve(1, 1) == 1         # уже на месте
    assert solve(1, 7) == 1
    assert solve(7, 1) == 1
    assert solve(2, 2) == 2
    assert solve(3, 4) == 10
    assert solve(4, 3) == 10        # симметрия
    assert solve(18, 18) == 2333606220
    with pytest.raises(ValueError):
        solve(0, 3)


@pytest.mark.parametrize("solve", PATHS)
def test_matrix_pathways_brute(solve):
    for rows in range(1, 8):
        for cols in range(1, 8):
            assert solve(rows, cols) == _paths_brute(rows, cols)


# ---------- neighborhood_burglary ----------

BURGLARY = [neighborhood_burglary_table, neighborhood_burglary]


def _burglary_brute(houses):
    best = 0
    indexes = range(len(houses))
    for size in range(len(houses) + 1):
        for chosen in combinations(indexes, size):
            if all(b - a > 1 for a, b in zip(chosen, chosen[1:])):
                best = max(best, sum(houses[i] for i in chosen))
    return best


@pytest.mark.parametrize("solve", BURGLARY)
def test_neighborhood_burglary_examples(solve):
    assert solve([60, 90, 50, 20, 80]) == 190       # 60 + 50 + 80
    assert solve([10, 100, 10]) == 100              # «через один» — не всегда ответ
    assert solve([70, 10, 10, 70]) == 140           # пропускаем сразу два дома
    assert solve([40]) == 40
    assert solve([40, 45]) == 45
    assert solve([]) == 0
    assert solve([0, 0, 0]) == 0


@pytest.mark.parametrize("solve", BURGLARY)
def test_neighborhood_burglary_random(solve):
    for _ in range(ROUNDS):
        houses = [RNG.randint(0, 50) for _ in range(RNG.randint(0, 10))]
        assert solve(houses) == _burglary_brute(houses)


# ---------- longest_common_subsequence ----------

LCS = [longest_common_subsequence, longest_common_subsequence_two_rows]


def _is_subsequence(small, big):
    rest = iter(big)
    return all(symbol in rest for symbol in small)


def _lcs_brute(first, second):
    if len(first) > len(second):
        first, second = second, first
    for size in range(len(first), -1, -1):
        for picked in combinations(first, size):
            if _is_subsequence(picked, second):
                return size
    return 0


@pytest.mark.parametrize("solve", LCS)
def test_longest_common_subsequence_examples(solve):
    assert solve("кабан", "банка") == 3             # «бан»
    assert solve("bdcab", "cbad") == 2
    assert solve("abc", "abc") == 3
    assert solve("abc", "xyz") == 0
    assert solve("abc", "cba") == 1                 # порядок важен
    assert solve("", "abc") == 0
    assert solve("abc", "") == 0
    assert solve("", "") == 0
    assert solve("aaaa", "aa") == 2


@pytest.mark.parametrize("solve", LCS)
def test_longest_common_subsequence_random(solve):
    for _ in range(ROUNDS):
        first = "".join(RNG.choice("abc") for _ in range(RNG.randint(0, 8)))
        second = "".join(RNG.choice("abc") for _ in range(RNG.randint(0, 8)))
        assert solve(first, second) == _lcs_brute(first, second)


def test_restore_common_subsequence():
    assert restore_common_subsequence("кабан", "банка") == "бан"
    assert restore_common_subsequence("abc", "xyz") == ""
    for _ in range(ROUNDS):
        first = "".join(RNG.choice("abc") for _ in range(RNG.randint(0, 8)))
        second = "".join(RNG.choice("abc") for _ in range(RNG.randint(0, 8)))
        common = restore_common_subsequence(first, second)
        assert len(common) == _lcs_brute(first, second)
        assert _is_subsequence(common, first) and _is_subsequence(common, second)


# ---------- longest_palindrome_in_a_string ----------

PALINDROME = [longest_palindrome_in_a_string_table, longest_palindrome_in_a_string]


def _palindrome_brute(text):
    """Все подстроки от длинных к коротким, слева направо — первая подошедшая и есть ответ."""
    for length in range(len(text), 0, -1):
        for start in range(len(text) - length + 1):
            piece = text[start:start + length]
            if piece == piece[::-1]:
                return piece
    return ""


@pytest.mark.parametrize("solve", PALINDROME)
def test_longest_palindrome_examples(solve):
    assert solve("перетоппот") == "топпот"          # чётная длина
    assert solve("xracecary") == "racecar"          # нечётная длина
    assert solve("abcd") == "a"                     # при равенстве — самый левый
    assert solve("zzzz") == "zzzz"
    assert solve("ab") == "a"
    assert solve("q") == "q"
    assert solve("") == ""
    assert solve("abacdfgdcaba") == "aba"           # «зеркальные» края не обманывают


@pytest.mark.parametrize("solve", PALINDROME)
def test_longest_palindrome_random(solve):
    for _ in range(ROUNDS):
        text = "".join(RNG.choice("ab" if RNG.random() < 0.5 else "abc") for _ in range(RNG.randint(0, 12)))
        assert solve(text) == _palindrome_brute(text)


# ---------- maximum_subarray_sum ----------

def _subarray_brute(nums):
    return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))


def test_maximum_subarray_sum_examples():
    assert maximum_subarray_sum([4, -6, 3, -1, 5, -8, 2]) == 7      # [3, -1, 5]
    assert maximum_subarray_sum([-5, -2, -9]) == -2                 # все отрицательные
    assert maximum_subarray_sum([1, 2, 3]) == 6                     # весь массив
    assert maximum_subarray_sum([-4]) == -4
    assert maximum_subarray_sum([0, 0]) == 0
    assert maximum_subarray_sum([6, -5, 6]) == 7                    # яму выгодно «перешагнуть»
    with pytest.raises(ValueError):
        maximum_subarray_sum([])
    with pytest.raises(ValueError):
        maximum_subarray_with_bounds([])


def test_maximum_subarray_with_bounds_examples():
    assert maximum_subarray_with_bounds([4, -6, 3, -1, 5, -8, 2]) == (7, 2, 4)
    assert maximum_subarray_with_bounds([-5, -2, -9]) == (-2, 1, 1)


def test_maximum_subarray_sum_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-10, 10) for _ in range(RNG.randint(1, 12))]
        expected = _subarray_brute(nums)
        assert maximum_subarray_sum(nums) == expected
        total, start, end = maximum_subarray_with_bounds(nums)
        assert total == expected
        assert 0 <= start <= end < len(nums)
        assert sum(nums[start:end + 1]) == expected


# ---------- zero_one_knapsack ----------

KNAPSACK = [zero_one_knapsack_table, zero_one_knapsack]


def _knapsack_brute(capacity, weights, values):
    best = 0
    for mask in product((False, True), repeat=len(weights)):
        if sum(w for w, taken in zip(weights, mask) if taken) <= capacity:
            best = max(best, sum(v for v, taken in zip(values, mask) if taken))
    return best


@pytest.mark.parametrize("solve", KNAPSACK)
def test_zero_one_knapsack_examples(solve):
    assert solve(6, [2, 3, 4], [30, 40, 60]) == 90          # предметы 0 и 2
    # Ловушка для обхода слева направо: лёгкий предмет нельзя взять трижды.
    assert solve(6, [2], [30]) == 30
    # Жадность по «ценности на килограмм» ошибается: берёт предмет 0 и упирается.
    assert solve(10, [6, 5, 5], [66, 50, 50]) == 100
    assert solve(3, [4, 5], [10, 20]) == 0                  # ничего не влезает
    assert solve(0, [1, 2], [10, 20]) == 0
    assert solve(5, [], []) == 0
    assert solve(5, [5], [8]) == 8                          # ровно по вместимости
    assert solve(4, [0, 4], [7, 9]) == 16                   # невесомый предмет берём всегда


@pytest.mark.parametrize("solve", KNAPSACK)
def test_zero_one_knapsack_rejects_bad_input(solve):
    with pytest.raises(ValueError):
        solve(5, [1, 2], [10])
    with pytest.raises(ValueError):
        solve(-1, [1], [10])


@pytest.mark.parametrize("solve", KNAPSACK)
def test_zero_one_knapsack_random(solve):
    for _ in range(ROUNDS):
        count = RNG.randint(0, 8)
        weights = [RNG.randint(0, 9) for _ in range(count)]
        values = [RNG.randint(0, 30) for _ in range(count)]
        capacity = RNG.randint(0, 20)
        assert solve(capacity, weights, values) == _knapsack_brute(capacity, weights, values)


def test_zero_one_knapsack_items():
    assert zero_one_knapsack_items(6, [2, 3, 4], [30, 40, 60]) == [0, 2]
    assert zero_one_knapsack_items(3, [4, 5], [10, 20]) == []
    for _ in range(ROUNDS):
        count = RNG.randint(0, 8)
        weights = [RNG.randint(1, 9) for _ in range(count)]
        values = [RNG.randint(0, 30) for _ in range(count)]
        capacity = RNG.randint(0, 20)
        chosen = zero_one_knapsack_items(capacity, weights, values)
        assert chosen == sorted(set(chosen))                 # каждый предмет не больше раза
        assert sum(weights[i] for i in chosen) <= capacity
        assert sum(values[i] for i in chosen) == _knapsack_brute(capacity, weights, values)

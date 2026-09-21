"""Тесты к паттерну Hash Maps and Sets.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор медленный, зато очевидно правильный.
"""

import copy
import random
from itertools import combinations

import pytest

from geometric_sequence_triplets import geometric_sequence_triplets
from longest_chain_of_consecutive_numbers import longest_chain_of_consecutive_numbers
from pair_sum_unsorted import pair_sum_unsorted
from verify_sudoku_board import verify_sudoku_board
from zero_striping import zero_striping, zero_striping_in_place

RNG = random.Random(2024)
ROUNDS = 500


# ---------- pair_sum_unsorted ----------

def test_pair_sum_unsorted_examples():
    assert pair_sum_unsorted([8, -3, 5, 1], 6) == [2, 3]
    assert pair_sum_unsorted([4, 4], 8) == [0, 1]
    assert pair_sum_unsorted([4], 8) == []          # элемент не пара сам себе
    assert pair_sum_unsorted([1, 2, 3], 100) == []
    assert pair_sum_unsorted([], 0) == []


def test_pair_sum_unsorted_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-10, 10) for _ in range(RNG.randint(0, 8))]
        target = RNG.randint(-20, 20)
        exists = any(a + b == target for a, b in combinations(nums, 2))
        answer = pair_sum_unsorted(nums, target)
        if exists:
            i, j = answer
            assert i != j and nums[i] + nums[j] == target
        else:
            assert answer == []


# ---------- geometric_sequence_triplets ----------

def _triplets_brute(nums, ratio):
    return sum(
        1
        for i, j, k in combinations(range(len(nums)), 3)
        if nums[j] == nums[i] * ratio and nums[k] == nums[j] * ratio
    )


def test_geometric_sequence_triplets_examples():
    assert geometric_sequence_triplets([3, 6, 6, 12, 5], 2) == 2
    assert geometric_sequence_triplets([7, 7, 7, 7], 1) == 4      # C(4, 3)
    assert geometric_sequence_triplets([1, -3, 9], -3) == 1
    assert geometric_sequence_triplets([12, 6, 3], 2) == 0        # порядок важен
    assert geometric_sequence_triplets([0, 0, 0], 5) == 1
    assert geometric_sequence_triplets([], 2) == 0
    assert geometric_sequence_triplets([1, 2], 2) == 0


def test_geometric_sequence_triplets_rejects_zero_ratio():
    with pytest.raises(ValueError):
        geometric_sequence_triplets([1, 2, 3], 0)


def test_geometric_sequence_triplets_random():
    for _ in range(ROUNDS):
        nums = [RNG.choice([-4, -2, -1, 0, 1, 2, 4, 8]) for _ in range(RNG.randint(0, 9))]
        ratio = RNG.choice([-2, -1, 1, 2, 3])
        assert geometric_sequence_triplets(nums, ratio) == _triplets_brute(nums, ratio)


# ---------- verify_sudoku_board ----------

VALID_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def _sudoku_brute(board):
    groups = []
    groups += [list(row) for row in board]
    groups += [[board[r][c] for r in range(9)] for c in range(9)]
    groups += [
        [board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
        for br in (0, 3, 6) for bc in (0, 3, 6)
    ]
    for group in groups:
        digits = [d for d in group if d != 0]
        if len(digits) != len(set(digits)):
            return False
    return True


def test_verify_sudoku_board_examples():
    assert verify_sudoku_board(VALID_BOARD)
    assert verify_sudoku_board([[0] * 9 for _ in range(9)])

    same_row = copy.deepcopy(VALID_BOARD)
    same_row[0][8] = 5
    assert not verify_sudoku_board(same_row)

    same_col = copy.deepcopy(VALID_BOARD)
    same_col[8][0] = 5
    assert not verify_sudoku_board(same_col)

    # Разные строки и столбцы, но один квадрат 3x3.
    same_box = copy.deepcopy(VALID_BOARD)
    same_box[2][0] = 3
    assert not verify_sudoku_board(same_box)


def test_verify_sudoku_board_random():
    for _ in range(ROUNDS):
        board = copy.deepcopy(VALID_BOARD)
        for _ in range(RNG.randint(0, 3)):
            board[RNG.randrange(9)][RNG.randrange(9)] = RNG.randint(0, 9)
        assert verify_sudoku_board(board) == _sudoku_brute(board)


# ---------- zero_striping ----------

def _striping_brute(matrix):
    m, n = len(matrix), len(matrix[0]) if matrix else 0
    return [
        [
            0 if any(matrix[r][j] == 0 for j in range(n))
            or any(matrix[i][c] == 0 for i in range(m))
            else matrix[r][c]
            for c in range(n)
        ]
        for r in range(m)
    ]


@pytest.mark.parametrize("solve", [zero_striping, zero_striping_in_place])
def test_zero_striping_examples(solve):
    matrix = [
        [4, 7, 2, 9],
        [5, 0, 8, 1],
        [3, 6, 1, 0],
    ]
    solve(matrix)
    assert matrix == [
        [4, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    # Ноль в углу: страдают и первая строка, и первый столбец.
    corner = [[0, 2], [3, 4]]
    solve(corner)
    assert corner == [[0, 0], [0, 4]]

    # Ноль в первой строке не должен обнулять первый столбец.
    top = [[1, 0, 3], [4, 5, 6]]
    solve(top)
    assert top == [[0, 0, 0], [4, 0, 6]]

    for trivial in ([], [[]], [[7]], [[0]]):
        solve(trivial)  # не падает


@pytest.mark.parametrize("solve", [zero_striping, zero_striping_in_place])
def test_zero_striping_random(solve):
    for _ in range(ROUNDS):
        m, n = RNG.randint(1, 5), RNG.randint(1, 5)
        matrix = [[RNG.choice([0, 1, 2, 3, 4, 5]) for _ in range(n)] for _ in range(m)]
        expected = _striping_brute(matrix)
        solve(matrix)
        assert matrix == expected


# ---------- longest_chain_of_consecutive_numbers ----------

def _chain_brute(nums):
    values = set(nums)
    best = 0
    for start in values:
        length = 0
        while start + length in values:
            length += 1
        best = max(best, length)
    return best


def test_longest_chain_examples():
    assert longest_chain_of_consecutive_numbers([10, 4, 12, 5, 3, 11, 6]) == 4
    assert longest_chain_of_consecutive_numbers([2, 2, 3, 3, 4]) == 3   # дубликаты
    assert longest_chain_of_consecutive_numbers([-1, 0, 1]) == 3
    assert longest_chain_of_consecutive_numbers([42]) == 1
    assert longest_chain_of_consecutive_numbers([]) == 0


def test_longest_chain_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-8, 8) for _ in range(RNG.randint(0, 12))]
        assert longest_chain_of_consecutive_numbers(nums) == _chain_brute(nums)


def test_longest_chain_is_linear_on_long_chain():
    # Наивный запуск подсчёта от каждого элемента здесь был бы O(n^2).
    assert longest_chain_of_consecutive_numbers(list(range(200_000))) == 200_000

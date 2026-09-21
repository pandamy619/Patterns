"""Тесты к теме Math and Geometry.

Кроме ручных примеров каждое решение сверяется с медленным, но очевидно
правильным эталоном на случайных данных: обход с матрицей посещённых клеток,
разворот через строку, перебор всех пар точек, симуляция круга, перебор троек.
"""

import random
from itertools import combinations

import pytest

from maximum_collinear_points import maximum_collinear_points
from reverse_32_bit_integer import INT_MAX, INT_MIN, reverse_32_bit_integer
from spiral_traversal import spiral_traversal
from the_josephus_problem import (
    the_josephus_problem,
    the_josephus_problem_iterative,
)
from triangle_numbers import triangle_numbers

RNG = random.Random(2024)
ROUNDS = 400


# ---------- spiral_traversal ----------

def _spiral_brute(matrix):
    """Идём, пока можем; упёрлись в край или посещённую клетку — поворачиваем."""
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    turns = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = heading = 0
    order = []
    for _ in range(rows * cols):
        order.append(matrix[r][c])
        visited[r][c] = True
        nr, nc = r + turns[heading][0], c + turns[heading][1]
        if not (0 <= nr < rows and 0 <= nc < cols) or visited[nr][nc]:
            heading = (heading + 1) % 4
            nr, nc = r + turns[heading][0], c + turns[heading][1]
        r, c = nr, nc
    return order


def test_spiral_traversal_examples():
    matrix = [
        [11, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
    ]
    assert spiral_traversal(matrix) == [11, 12, 13, 14, 24, 34, 33, 32, 31, 21, 22, 23]
    assert spiral_traversal([[1, 2], [4, 3]]) == [1, 2, 3, 4]
    assert spiral_traversal([[5, 6, 7]]) == [5, 6, 7]            # одна строка
    assert spiral_traversal([[5], [6], [7]]) == [5, 6, 7]        # один столбец
    assert spiral_traversal([[1, 2], [6, 3], [5, 4]]) == [1, 2, 3, 4, 5, 6]
    assert spiral_traversal([[9]]) == [9]
    assert spiral_traversal([]) == []
    assert spiral_traversal([[]]) == []


def test_spiral_traversal_random():
    for _ in range(ROUNDS):
        rows, cols = RNG.randint(1, 7), RNG.randint(1, 7)
        matrix = [[RNG.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]
        snapshot = [row[:] for row in matrix]
        assert spiral_traversal(matrix) == _spiral_brute(matrix)
        assert matrix == snapshot, "матрицу менять нельзя"


# ---------- reverse_32_bit_integer ----------

def _reverse_brute(n):
    sign = -1 if n < 0 else 1
    value = sign * int(str(abs(n))[::-1])
    return value if INT_MIN <= value <= INT_MAX else 0


def test_reverse_32_bit_integer_examples():
    assert reverse_32_bit_integer(9051) == 1509
    assert reverse_32_bit_integer(-47) == -74
    assert reverse_32_bit_integer(7300) == 37             # ведущие нули пропадают
    assert reverse_32_bit_integer(-600) == -6
    assert reverse_32_bit_integer(0) == 0
    assert reverse_32_bit_integer(8) == 8
    assert reverse_32_bit_integer(-3) == -3


def test_reverse_32_bit_integer_overflow_edges():
    assert reverse_32_bit_integer(INT_MAX) == 0           # 7463847412 не влезает
    assert reverse_32_bit_integer(INT_MIN) == 0           # и abs() тут не спасает
    assert reverse_32_bit_integer(1_000_000_009) == 0
    assert reverse_32_bit_integer(-1_000_000_009) == 0
    # Вплотную к границам с обеих сторон.
    assert reverse_32_bit_integer(1_463_847_412) == 2_147_483_641
    assert reverse_32_bit_integer(-1_463_847_412) == -2_147_483_641
    assert reverse_32_bit_integer(2_147_483_412) == 2_143_847_412
    assert reverse_32_bit_integer(1_563_847_412) == 0     # 2147483651 > INT_MAX
    assert reverse_32_bit_integer(-1_563_847_412) == 0


def test_reverse_32_bit_integer_random():
    for _ in range(ROUNDS):
        # Половина чисел короткие, половина — во весь 32-битный диапазон,
        # иначе переполнение почти не встречается.
        if RNG.random() < 0.5:
            n = RNG.randint(-99_999, 99_999)
        else:
            n = RNG.randint(INT_MIN, INT_MAX)
        assert reverse_32_bit_integer(n) == _reverse_brute(n)


# ---------- maximum_collinear_points ----------

def _collinear_brute(points):
    """Каждая пара задаёт прямую; считаем точки на ней векторным произведением."""
    if len(points) <= 2:
        return len(points)
    best = 2
    for (ax, ay), (bx, by) in combinations(points, 2):
        on_line = sum(
            1 for cx, cy in points
            if (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) == 0
        )
        best = max(best, on_line)
    return best


def test_maximum_collinear_points_examples():
    points = [[0, 1], [2, 2], [4, 3], [1, 4], [6, 4], [4, 0]]
    assert maximum_collinear_points(points) == 4          # прямая y = x/2 + 1
    assert maximum_collinear_points([]) == 0
    assert maximum_collinear_points([[3, 3]]) == 1
    assert maximum_collinear_points([[3, 3], [-5, 8]]) == 2
    assert maximum_collinear_points([[0, 0], [1, 0], [0, 1]]) == 2


def test_maximum_collinear_points_special_lines():
    vertical = [[2, -3], [2, 0], [2, 5], [2, 9], [0, 0], [1, 1]]
    assert maximum_collinear_points(vertical) == 4
    horizontal = [[-4, 7], [0, 7], [3, 7], [1, 1], [2, 5]]
    assert maximum_collinear_points(horizontal) == 3
    # Опорная точка посередине: направления (1, 2) и (-1, -2) — одна прямая.
    through_middle = [[0, 0], [-1, -2], [1, 2], [-2, -4], [5, 1]]
    assert maximum_collinear_points(through_middle) == 4
    # Убывающая прямая: знак нормализуется и тут.
    falling = [[0, 6], [2, 3], [4, 0], [-2, 9], [1, 1]]
    assert maximum_collinear_points(falling) == 4


def test_maximum_collinear_points_float_trap():
    # Наклоны 10**9 / (10**9 - 1) и (10**9 + 1) / 10**9 различны,
    # но после деления во float совпадают. Три точки НЕ на одной прямой.
    big = 10**9
    assert big / (big - 1) == (big + 1) / big             # вот она, ловушка
    points = [(0, 0), (big - 1, big), (big, big + 1)]
    assert maximum_collinear_points(points) == 2


def test_maximum_collinear_points_random():
    for _ in range(ROUNDS):
        # Маленькая сетка — чтобы коллинеарные тройки встречались часто.
        cells = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
        points = RNG.sample(cells, RNG.randint(0, 10))
        assert maximum_collinear_points(points) == _collinear_brute(points)


# ---------- the_josephus_problem ----------

def _josephus_brute(n, k):
    """Честная симуляция: отсчитываем k человек и удаляем последнего."""
    circle = list(range(n))
    start = 0
    while len(circle) > 1:
        out = (start + k - 1) % len(circle)
        circle.pop(out)
        start = out              # на место выбывшего сдвинулся следующий
    return circle[0]


def test_the_josephus_problem_examples():
    for solve in (the_josephus_problem, the_josephus_problem_iterative):
        assert solve(6, 4) == 4
        assert solve(1, 1) == 0
        assert solve(1, 50) == 0
        assert solve(5, 1) == 4          # выбывают подряд, остаётся последний
        assert solve(2, 2) == 0
        assert solve(2, 3) == 1          # k больше n — счёт идёт по кругу
        assert solve(7, 2) == 6


def test_the_josephus_problem_rejects_bad_input():
    for solve in (the_josephus_problem, the_josephus_problem_iterative):
        with pytest.raises(ValueError):
            solve(0, 3)
        with pytest.raises(ValueError):
            solve(4, 0)


def test_the_josephus_problem_iterative_handles_large_n():
    # Рекурсивный вариант здесь упал бы с RecursionError.
    n = 200_000
    answer = the_josephus_problem_iterative(n, 2)
    # Для k = 2 есть замкнутая формула: n = 2**m + rest -> 2 * rest (с нуля).
    rest = n - (1 << (n.bit_length() - 1))
    assert answer == 2 * rest


def test_the_josephus_problem_random():
    for _ in range(ROUNDS):
        n, k = RNG.randint(1, 40), RNG.randint(1, 60)
        expected = _josephus_brute(n, k)
        assert the_josephus_problem(n, k) == expected
        assert the_josephus_problem_iterative(n, k) == expected


# ---------- triangle_numbers ----------

def _triangles_brute(lengths):
    return sum(
        1 for a, b, c in combinations(lengths, 3)
        if a + b > c and a + c > b and b + c > a
    )


def test_triangle_numbers_examples():
    assert triangle_numbers([7, 3, 5, 10, 4]) == 5
    assert triangle_numbers([2, 2, 2, 2]) == 4            # тройки различаются индексами
    assert triangle_numbers([1, 2, 3]) == 0               # вырожденный: 1 + 2 == 3
    assert triangle_numbers([0, 5, 5]) == 0               # нулевая сторона
    assert triangle_numbers([0, 0, 0]) == 0
    assert triangle_numbers([1, 1, 100]) == 0
    assert triangle_numbers([4, 6]) == 0
    assert triangle_numbers([]) == 0


def test_triangle_numbers_does_not_mutate_input():
    lengths = [9, 2, 7, 4]
    triangle_numbers(lengths)
    assert lengths == [9, 2, 7, 4]


def test_triangle_numbers_random():
    for _ in range(ROUNDS):
        lengths = [RNG.randint(0, 12) for _ in range(RNG.randint(0, 10))]
        assert triangle_numbers(lengths) == _triangles_brute(lengths)

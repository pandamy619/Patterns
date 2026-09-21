"""Тесты к паттерну Sort and Search.

Кроме ручных примеров каждое решение сверяется с эталоном на случайных данных.
Эталон — встроенная sorted: в самих решениях она запрещена, а в тестах это
как раз «очевидно правильная» реализация, в которой негде ошибиться.
"""

import random
import sys

import pytest

from dutch_national_flag import dutch_national_flag
from kth_largest_integer import kth_largest_integer, kth_largest_integer_heap
from sort_and_search_helpers import ListNode, build_list, iter_nodes, to_values
from sort_array import partition_three_way, sort_array, sort_array_counting
from sort_linked_list import sort_linked_list, sort_linked_list_bottom_up

RNG = random.Random(2024)
ROUNDS = 400

LIST_SORTERS = [sort_linked_list, sort_linked_list_bottom_up]
KTH_SOLVERS = [kth_largest_integer, kth_largest_integer_heap]


# ---------- sort_linked_list ----------

@pytest.mark.parametrize("sort_list", LIST_SORTERS)
def test_sort_linked_list_examples(sort_list):
    assert to_values(sort_list(build_list([7, 2, 9, 4, 1]))) == [1, 2, 4, 7, 9]
    assert to_values(sort_list(build_list([3, -5, 3, 0, -5]))) == [-5, -5, 0, 3, 3]
    assert to_values(sort_list(build_list([1, 2, 3, 4]))) == [1, 2, 3, 4]      # уже отсортирован
    assert to_values(sort_list(build_list([4, 3, 2, 1]))) == [1, 2, 3, 4]      # в обратном порядке
    assert to_values(sort_list(build_list([6, 6, 6]))) == [6, 6, 6]


@pytest.mark.parametrize("sort_list", LIST_SORTERS)
def test_sort_linked_list_edge_cases(sort_list):
    assert sort_list(None) is None
    single = ListNode(42)
    assert sort_list(single) is single
    assert to_values(sort_list(build_list([2, 1]))) == [1, 2]    # два узла: деление 1 + 1
    assert to_values(sort_list(build_list([2, 3, 1]))) == [1, 2, 3]


@pytest.mark.parametrize("sort_list", LIST_SORTERS)
def test_sort_linked_list_reuses_nodes_and_is_stable(sort_list):
    for _ in range(ROUNDS):
        # Узкий диапазон значений — чтобы дубликатов было много.
        head = build_list(RNG.randint(0, 4) for _ in range(RNG.randint(0, 12)))
        position = {id(node): index for index, node in enumerate(iter_nodes(head))}

        nodes_after = list(iter_nodes(sort_list(head)))

        # Те же самые узлы, ни одного нового и ни одного потерянного.
        assert sorted(id(node) for node in nodes_after) == sorted(position)
        # Стабильность: при сортировке по паре (значение, исходная позиция)
        # получился бы ровно тот же порядок.
        keys = [(node.val, position[id(node)]) for node in nodes_after]
        assert keys == sorted(keys)


@pytest.mark.parametrize("sort_list", LIST_SORTERS)
def test_sort_linked_list_random(sort_list):
    for _ in range(ROUNDS):
        values = [RNG.randint(-20, 20) for _ in range(RNG.randint(0, 40))]
        assert to_values(sort_list(build_list(values))) == sorted(values)


@pytest.mark.parametrize("sort_list", LIST_SORTERS)
def test_sort_linked_list_long_input_does_not_overflow_stack(sort_list):
    values = [RNG.randint(-10**6, 10**6) for _ in range(30_000)]
    assert to_values(sort_list(build_list(values))) == sorted(values)
    # Отсортированный вход — худший случай для наивных реализаций.
    assert to_values(sort_list(build_list(range(30_000)))) == list(range(30_000))


# ---------- sort_array: partition ----------

def test_partition_three_way_example():
    nums = [5, 9, 5, 2, 8, 1, 5, 7]
    assert partition_three_way(nums, 0, len(nums) - 1, 5) == (2, 4)
    assert nums == [2, 1, 5, 5, 5, 8, 7, 9]


def test_partition_three_way_touches_only_its_range():
    nums = [100, 3, 1, 2, -100]
    assert partition_three_way(nums, 1, 3, 2) == (2, 2)
    assert nums == [100, 1, 2, 3, -100]


def test_partition_three_way_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(0, 6) for _ in range(RNG.randint(1, 12))]
        lo = RNG.randint(0, len(nums) - 1)
        hi = RNG.randint(lo, len(nums) - 1)
        pivot = nums[RNG.randint(lo, hi)]
        before = list(nums)

        lt, gt = partition_three_way(nums, lo, hi, pivot)

        assert lo <= lt <= gt <= hi
        assert all(value < pivot for value in nums[lo:lt])
        assert all(value == pivot for value in nums[lt:gt + 1])
        assert all(value > pivot for value in nums[gt + 1:hi + 1])
        assert sorted(nums[lo:hi + 1]) == sorted(before[lo:hi + 1])
        assert nums[:lo] == before[:lo] and nums[hi + 1:] == before[hi + 1:]


# ---------- sort_array: quicksort ----------

def test_sort_array_examples():
    assert sort_array([9, 4, 7, 1, 8, 2]) == [1, 2, 4, 7, 8, 9]
    assert sort_array([0, -3, 5, -3, 0]) == [-3, -3, 0, 0, 5]
    assert sort_array([]) == []
    assert sort_array([1]) == [1]
    assert sort_array([2, 1]) == [1, 2]
    assert sort_array([4, 4, 4, 4]) == [4, 4, 4, 4]


def test_sort_array_works_in_place():
    nums = [3, 1, 2]
    assert sort_array(nums) is nums
    assert nums == [1, 2, 3]


def test_sort_array_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-30, 30) for _ in range(RNG.randint(0, 50))]
        assert sort_array(list(nums)) == sorted(nums)


@pytest.mark.parametrize(
    "make",
    [
        lambda n: list(range(n)),                 # отсортирован
        lambda n: list(range(n, 0, -1)),          # в обратном порядке
        lambda n: [7] * n,                        # все элементы равны
        lambda n: [i % 3 for i in range(n)],      # всего три разных значения
        lambda n: list(range(n // 2)) + list(range(n // 2, 0, -1)),   # «горка»
    ],
)
def test_sort_array_survives_adversarial_inputs(make):
    # Наивный quicksort (опорный = последний, две зоны) на таких входах делает
    # O(n²) сравнений и уходит в рекурсию глубиной n. Лимит рекурсии занижаем,
    # чтобы тест падал сразу, если глубина стека перестанет быть логарифмической.
    nums = make(20_000)
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(200)
    try:
        assert sort_array(list(nums)) == sorted(nums)
    finally:
        sys.setrecursionlimit(old_limit)


# ---------- sort_array: counting sort ----------

def test_sort_array_counting_examples():
    assert sort_array_counting([3, -1, 2, 3, 0, -1, 3]) == [-1, -1, 0, 2, 3, 3, 3]
    assert sort_array_counting([]) == []
    assert sort_array_counting([5]) == [5]
    assert sort_array_counting([-7, -7]) == [-7, -7]
    assert sort_array_counting([10**9, 10**9 - 2]) == [10**9 - 2, 10**9]   # важен диапазон, а не величина


def test_sort_array_counting_does_not_modify_input():
    nums = [2, 0, 1]
    assert sort_array_counting(nums) == [0, 1, 2]
    assert nums == [2, 0, 1]


def test_sort_array_counting_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-15, 15) for _ in range(RNG.randint(0, 50))]
        assert sort_array_counting(nums) == sorted(nums)


# ---------- kth_largest_integer ----------

@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_examples(solve):
    nums = [14, 3, 22, 8, 17, 5, 11]
    assert solve(nums, 1) == 22
    assert solve(nums, 3) == 14
    assert solve(nums, 7) == 3
    assert solve([9], 1) == 9
    assert solve([-4, -9, -1], 2) == -4


@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_counts_duplicates_separately(solve):
    nums = [6, 2, 6, 9, 2, 6]          # по убыванию: 9 6 6 6 2 2
    assert [solve(nums, k) for k in range(1, 7)] == [9, 6, 6, 6, 2, 2]


@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_does_not_modify_input(solve):
    nums = [4, 1, 3, 2]
    solve(nums, 2)
    assert nums == [4, 1, 3, 2]


@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_rejects_bad_k(solve):
    for nums, k in [([1, 2, 3], 0), ([1, 2, 3], 4), ([1, 2, 3], -1), ([], 1)]:
        with pytest.raises(ValueError):
            solve(nums, k)


@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_random(solve):
    for _ in range(ROUNDS):
        nums = [RNG.randint(-12, 12) for _ in range(RNG.randint(1, 30))]
        k = RNG.randint(1, len(nums))
        assert solve(nums, k) == sorted(nums, reverse=True)[k - 1]


@pytest.mark.parametrize("solve", KTH_SOLVERS)
def test_kth_largest_integer_large_inputs(solve):
    n = 50_000
    assert solve(list(range(n)), n // 2) == n - n // 2       # отсортированный вход
    assert solve([5] * n, n // 2) == 5                        # все равны: у двухзонного разбиения тут O(n²)


# ---------- dutch_national_flag ----------

def test_dutch_national_flag_examples():
    cases = [
        [2, 0, 1, 2, 1, 0, 0],
        [],
        [1],
        [2, 2, 2],
        [0, 1, 2],
        [2, 1, 0],
        [1, 0],
    ]
    for nums in cases:
        expected = sorted(nums)
        assert dutch_national_flag(nums) is None     # работает на месте
        assert nums == expected


def test_dutch_national_flag_rejects_foreign_values():
    with pytest.raises(ValueError):
        dutch_national_flag([0, 3, 1])


def test_dutch_national_flag_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(0, 2) for _ in range(RNG.randint(0, 25))]
        expected = sorted(nums)
        dutch_national_flag(nums)
        assert nums == expected

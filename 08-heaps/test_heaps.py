"""Тесты к паттерну Heaps.

Кроме ручных примеров каждое решение сверяется с очевидно правильной
наивной реализацией на случайных данных: сортировка вместо кучи медленнее,
зато ошибиться в ней негде.
"""

import heapq
import random
import statistics
from collections import Counter

import pytest

from combine_sorted_linked_lists import combine_sorted_linked_lists
from heaps_helpers import ListNode, build_list, list_to_values
from k_most_frequent_strings import (
    k_most_frequent_strings_max_heap,
    k_most_frequent_strings_min_heap,
)
from median_of_an_integer_stream import MedianOfAnIntegerStream

RNG = random.Random(2024)
ROUNDS = 400

TOP_K_SOLVERS = [k_most_frequent_strings_max_heap, k_most_frequent_strings_min_heap]


# ---------- k_most_frequent_strings ----------

def _top_k_brute(strs, k):
    freqs = Counter(strs)
    ranked = sorted(freqs, key=lambda word: (-freqs[word], word))
    return ranked[:max(k, 0)]


@pytest.mark.parametrize("solve", TOP_K_SOLVERS)
def test_k_most_frequent_strings_examples(solve):
    words = ["tea", "milk", "tea", "jam", "milk", "tea", "rye", "jam"]
    assert solve(words, 2) == ["tea", "jam"]           # jam и milk по 2, jam раньше по алфавиту
    assert solve(words, 3) == ["tea", "jam", "milk"]
    assert solve(words, 4) == ["tea", "jam", "milk", "rye"]
    assert solve(words, 1) == ["tea"]


@pytest.mark.parametrize("solve", TOP_K_SOLVERS)
def test_k_most_frequent_strings_ties_are_alphabetical(solve):
    # Все частоты равны: ответ целиком определяется алфавитом.
    assert solve(["d", "b", "a", "c"], 3) == ["a", "b", "c"]
    # Префикс меньше более длинной строки; заглавные буквы идут раньше строчных.
    assert solve(["ab", "abc", "a", "B"], 4) == ["B", "a", "ab", "abc"]


@pytest.mark.parametrize("solve", TOP_K_SOLVERS)
def test_k_most_frequent_strings_edge_cases(solve):
    assert solve([], 3) == []
    assert solve(["x", "x"], 0) == []
    assert solve(["x", "x", "x"], 1) == ["x"]
    # Уникальных строк меньше, чем k, — возвращаем все, что есть.
    assert solve(["q", "p", "q"], 10) == ["q", "p"]


@pytest.mark.parametrize("solve", TOP_K_SOLVERS)
def test_k_most_frequent_strings_does_not_mutate_input(solve):
    words = ["b", "a", "b"]
    solve(words, 1)
    assert words == ["b", "a", "b"]


@pytest.mark.parametrize("solve", TOP_K_SOLVERS)
def test_k_most_frequent_strings_random(solve):
    alphabet = ["a", "b", "ab", "ba", "abc", "c", "ca", "z"]
    for _ in range(ROUNDS):
        strs = [RNG.choice(alphabet) for _ in range(RNG.randint(0, 20))]
        k = RNG.randint(0, 10)
        assert solve(strs, k) == _top_k_brute(strs, k)


# ---------- combine_sorted_linked_lists ----------

def _combine(list_of_values):
    heads = [build_list(values) for values in list_of_values]
    return list_to_values(combine_sorted_linked_lists(heads))


def test_list_nodes_are_not_comparable():
    # Причина, по которой в кортеже нужен tie-breaker: при равных значениях
    # сравнение кортежей добирается до узлов, а они «<» не поддерживают.
    heap = [(7, ListNode(7))]
    with pytest.raises(TypeError):
        heapq.heappush(heap, (7, ListNode(7)))


def test_combine_sorted_linked_lists_examples():
    # Три пятёрки из трёх разных списков одновременно оказываются в куче.
    assert _combine([[2, 5], [1, 5, 8], [5]]) == [1, 2, 5, 5, 5, 8]
    assert _combine([[2, 9], [1, 5, 5], [4]]) == [1, 2, 4, 5, 5, 9]
    assert _combine([[-3, 0], [-3, 0], [-3, 0]]) == [-3, -3, -3, 0, 0, 0]
    assert _combine([[1, 2, 3]]) == [1, 2, 3]
    assert _combine([[10, 20], [1, 2]]) == [1, 2, 10, 20]     # списки не пересекаются


def test_combine_sorted_linked_lists_empty_inputs():
    assert combine_sorted_linked_lists([]) is None
    assert combine_sorted_linked_lists([None]) is None
    assert combine_sorted_linked_lists([None, None, None]) is None
    assert _combine([[], [4, 6], [], [5]]) == [4, 5, 6]


def test_combine_sorted_linked_lists_all_values_equal():
    # Самый неприятный случай для кучи без tie-breaker'а.
    assert _combine([[8] * 5, [8] * 3, [8] * 4]) == [8] * 12


def test_combine_sorted_linked_lists_reuses_nodes():
    heads = [build_list([1, 4]), build_list([2, 3])]
    original_ids = set()
    for head in heads:
        node = head
        while node is not None:
            original_ids.add(id(node))
            node = node.next

    merged_ids = []
    node = combine_sorted_linked_lists(heads)
    while node is not None:
        merged_ids.append(id(node))
        node = node.next

    assert len(merged_ids) == 4
    assert set(merged_ids) == original_ids


def test_combine_sorted_linked_lists_random():
    for _ in range(ROUNDS):
        list_of_values = [
            sorted(RNG.randint(-6, 6) for _ in range(RNG.randint(0, 7)))
            for _ in range(RNG.randint(0, 6))
        ]
        expected = sorted(value for values in list_of_values for value in values)
        assert _combine(list_of_values) == expected


def test_combine_sorted_linked_lists_many_lists():
    # 2000 списков по одному узлу: с линейным поиском минимума вместо кучи
    # это было бы 2000 * 2000 сравнений.
    list_of_values = [[RNG.randint(0, 50)] for _ in range(2000)]
    expected = sorted(values[0] for values in list_of_values)
    assert _combine(list_of_values) == expected


# ---------- median_of_an_integer_stream ----------

def test_median_examples():
    stream = MedianOfAnIntegerStream()
    seen = []
    for num, expected in [(7, 7.0), (2, 4.5), (10, 7.0), (4, 5.5), (4, 4.0), (-1, 4.0)]:
        stream.add(num)
        seen.append(num)
        assert stream.get_median() == expected, seen
    assert len(stream) == 6


def test_median_returns_float():
    stream = MedianOfAnIntegerStream()
    stream.add(3)
    assert isinstance(stream.get_median(), float)
    stream.add(5)
    assert isinstance(stream.get_median(), float)
    assert stream.get_median() == 4.0


def test_median_of_empty_stream_is_an_error():
    with pytest.raises(ValueError):
        MedianOfAnIntegerStream().get_median()


@pytest.mark.parametrize(
    "numbers",
    [
        [5, 5, 5, 5],                 # одни дубликаты
        [1, 2, 3, 4, 5, 6, 7],        # возрастающий поток: всё время перебрасываем в lower
        [7, 6, 5, 4, 3, 2, 1],        # убывающий поток: перебрасываем в upper
        [-4, -9, 0, -1],              # отрицательные числа и приём с минусом
    ],
)
def test_median_special_streams(numbers):
    stream = MedianOfAnIntegerStream()
    for count, num in enumerate(numbers, start=1):
        stream.add(num)
        assert stream.get_median() == statistics.median(numbers[:count])


def test_median_random_with_invariants():
    for _ in range(ROUNDS):
        stream = MedianOfAnIntegerStream()
        seen = []
        for _ in range(RNG.randint(1, 25)):
            num = RNG.randint(-15, 15)
            stream.add(num)
            seen.append(num)
            assert stream.get_median() == statistics.median(seen)

            # Инварианты двух куч: размеры отличаются не больше чем на один
            # в пользу lower, и ни одно число из lower не больше чисел из upper.
            lower = [-value for value in stream._lower]
            upper = list(stream._upper)
            assert len(lower) - len(upper) in (0, 1)
            assert sorted(lower + upper) == sorted(seen)
            if upper:
                assert max(lower) <= min(upper)

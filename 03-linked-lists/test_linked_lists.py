"""Тесты к паттерну Linked Lists.

Кроме ручных примеров каждое решение сверяется с очевидно правильным
эталоном на случайных данных: со списками Python вместо узлов,
а LRU-кэш — с реализацией на OrderedDict.
"""

import random
from collections import OrderedDict

import pytest

from flatten_multi_level_linked_list import (
    flatten_multi_level_list,
    flatten_multi_level_list_depth_first,
)
from linked_list_intersection import (
    linked_list_intersection,
    linked_list_intersection_hash_set,
)
from linked_list_reversal import reverse_list, reverse_list_recursive
from linked_lists_helpers import MultiLevelNode, build_list, iter_nodes, to_values
from lru_cache_design import LRUCache
from palindrome_linked_list import palindrome_linked_list
from remove_kth_last_node import remove_kth_last_node

RNG = random.Random(2024)
ROUNDS = 400


# ---------- helpers ----------

def test_helpers_round_trip():
    assert build_list([]) is None
    assert to_values(None) == []
    assert to_values(build_list([5, 1, 5])) == [5, 1, 5]


# ---------- linked_list_reversal ----------

REVERSALS = [reverse_list, reverse_list_recursive]


@pytest.mark.parametrize("reverse", REVERSALS)
def test_reversal_examples(reverse):
    assert to_values(reverse(build_list([4, 9, 2, 7]))) == [7, 2, 9, 4]
    assert to_values(reverse(build_list([3, 3, 8]))) == [8, 3, 3]
    assert to_values(reverse(build_list([6]))) == [6]
    assert reverse(None) is None


@pytest.mark.parametrize("reverse", REVERSALS)
def test_reversal_reuses_nodes(reverse):
    # Разворот «на месте»: те же самые узлы, новых не создаём.
    head = build_list([1, 2, 3, 4, 5])
    before = list(iter_nodes(head))
    after = list(iter_nodes(reverse(head)))
    assert len(after) == len(before)
    assert all(x is y for x, y in zip(after, reversed(before)))
    assert head.next is None            # бывшая голова стала хвостом


@pytest.mark.parametrize("reverse", REVERSALS)
def test_reversal_random(reverse):
    for _ in range(ROUNDS):
        values = [RNG.randint(-9, 9) for _ in range(RNG.randint(0, 12))]
        assert to_values(reverse(build_list(values))) == values[::-1]


def test_reversal_iterative_handles_long_list():
    # Рекурсивный вариант здесь упёрся бы в лимит глубины рекурсии.
    values = list(range(50_000))
    assert to_values(reverse_list(build_list(values))) == values[::-1]


# ---------- remove_kth_last_node ----------

def _remove_kth_last_brute(values, k):
    if k > len(values):
        return list(values)
    index = len(values) - k
    return values[:index] + values[index + 1:]


def test_remove_kth_last_node_examples():
    assert to_values(remove_kth_last_node(build_list([5, 8, 3, 6, 1]), 2)) == [5, 8, 3, 1]
    assert to_values(remove_kth_last_node(build_list([5, 8, 3]), 1)) == [5, 8]      # хвост
    assert to_values(remove_kth_last_node(build_list([5, 8, 3]), 3)) == [8, 3]      # голова
    assert remove_kth_last_node(build_list([7]), 1) is None                         # единственный узел
    assert to_values(remove_kth_last_node(build_list([5, 8, 3]), 4)) == [5, 8, 3]   # k больше длины
    assert remove_kth_last_node(None, 1) is None


def test_remove_kth_last_node_rejects_bad_k():
    with pytest.raises(ValueError):
        remove_kth_last_node(build_list([1, 2]), 0)


def test_remove_kth_last_node_random():
    for _ in range(ROUNDS):
        values = [RNG.randint(0, 9) for _ in range(RNG.randint(0, 10))]
        k = RNG.randint(1, 12)
        result = remove_kth_last_node(build_list(values), k)
        assert to_values(result) == _remove_kth_last_brute(values, k)


# ---------- linked_list_intersection ----------

INTERSECTIONS = [linked_list_intersection, linked_list_intersection_hash_set]


def _with_shared_tail(own_a, own_b, shared):
    """Два списка с общим хвостом. Возвращает (head_a, head_b, первый общий узел)."""
    tail = build_list(shared)

    def attach(values):
        head = build_list(values)
        if head is None:
            return tail
        *_, last = iter_nodes(head)
        last.next = tail
        return head

    return attach(own_a), attach(own_b), tail


def _intersection_brute(head_a, head_b):
    for a in iter_nodes(head_a):
        for b in iter_nodes(head_b):
            if a is b:
                return a
    return None


@pytest.mark.parametrize("intersect", INTERSECTIONS)
def test_intersection_examples(intersect):
    head_a, head_b, joint = _with_shared_tail([2, 7], [9, 4, 1, 3], [6, 5])
    assert intersect(head_a, head_b) is joint
    assert intersect(head_b, head_a) is joint

    # Одинаковые значения — ещё не пересечение: сравниваются узлы.
    assert intersect(build_list([1, 2, 3]), build_list([1, 2, 3])) is None

    # Один список целиком является хвостом другого.
    head_a, head_b, joint = _with_shared_tail([8, 8], [], [4])
    assert head_b is joint
    assert intersect(head_a, head_b) is joint

    # Один и тот же список дважды.
    same = build_list([1, 2])
    assert intersect(same, same) is same

    assert intersect(None, build_list([1])) is None
    assert intersect(build_list([1]), None) is None
    assert intersect(None, None) is None


@pytest.mark.parametrize("intersect", INTERSECTIONS)
def test_intersection_random(intersect):
    for _ in range(ROUNDS):
        own_a = [RNG.randint(0, 3) for _ in range(RNG.randint(0, 6))]
        own_b = [RNG.randint(0, 3) for _ in range(RNG.randint(0, 6))]
        shared = [RNG.randint(0, 3) for _ in range(RNG.randint(0, 5))]
        head_a, head_b, _ = _with_shared_tail(own_a, own_b, shared)
        assert intersect(head_a, head_b) is _intersection_brute(head_a, head_b)


def test_intersection_does_not_modify_lists():
    head_a, head_b, _ = _with_shared_tail([2, 7], [9], [6, 5])
    linked_list_intersection(head_a, head_b)
    assert to_values(head_a) == [2, 7, 6, 5]
    assert to_values(head_b) == [9, 6, 5]


# ---------- lru_cache_design ----------

class _ReferenceLRU:
    """Эталон: OrderedDict сам помнит порядок, остаётся двигать ключи в конец."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        elif len(self.data) == self.capacity:
            self.data.popitem(last=False)
        self.data[key] = value


def test_lru_cache_example():
    cache = LRUCache(2)
    cache.put(7, 70)
    cache.put(3, 30)
    assert cache.get(7) == 70           # 7 стал свежим, на вылет теперь 3
    cache.put(5, 50)                    # вытесняет 3
    assert cache.get(3) == -1
    cache.put(7, 71)                    # обновление: размер прежний, 7 снова свежий
    assert len(cache) == 2
    cache.put(9, 90)                    # вытесняет 5, а не 7
    assert cache.get(5) == -1
    assert cache.get(7) == 71
    assert cache.get(9) == 90
    assert cache.items() == [(7, 71), (9, 90)]


def test_lru_cache_capacity_one():
    cache = LRUCache(1)
    assert cache.get(1) == -1
    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == -1
    assert cache.get(2) == 20
    assert len(cache) == 1


def test_lru_cache_rejects_bad_capacity():
    for capacity in (0, -3):
        with pytest.raises(ValueError):
            LRUCache(capacity)


def test_lru_cache_random_against_ordered_dict():
    for _ in range(ROUNDS):
        capacity = RNG.randint(1, 5)
        cache, reference = LRUCache(capacity), _ReferenceLRU(capacity)
        for _ in range(RNG.randint(0, 40)):
            key = RNG.randint(1, 8)
            if RNG.random() < 0.5:
                assert cache.get(key) == reference.get(key)
            else:
                value = RNG.randint(1, 1000)
                cache.put(key, value)
                reference.put(key, value)
            # Сверяем не только ответы, но и весь порядок вытеснения.
            assert cache.items() == list(reference.data.items())
            assert len(cache) == len(reference.data) <= capacity


# ---------- palindrome_linked_list ----------

def test_palindrome_examples():
    assert palindrome_linked_list(build_list([3, 8, 8, 3]))
    assert palindrome_linked_list(build_list([3, 8, 5, 8, 3]))
    assert not palindrome_linked_list(build_list([3, 8, 5, 3]))
    assert not palindrome_linked_list(build_list([1, 2]))
    assert palindrome_linked_list(build_list([4, 4]))
    assert palindrome_linked_list(build_list([4]))
    assert palindrome_linked_list(None)


def test_palindrome_random_and_list_is_restored():
    for _ in range(ROUNDS):
        values = [RNG.randint(0, 2) for _ in range(RNG.randint(0, 9))]
        head = build_list(values)
        nodes_before = list(iter_nodes(head))
        assert palindrome_linked_list(head) == (values == values[::-1])
        # Внутри половина списка разворачивалась — проверяем, что её вернули.
        nodes_after = list(iter_nodes(head))
        assert len(nodes_after) == len(nodes_before)
        assert all(x is y for x, y in zip(nodes_after, nodes_before))


# ---------- flatten_multi_level_linked_list ----------
#
# Описание многоуровневого списка в тестах — «ряд»: список пар
# (значение, дочерний ряд или None).

def _build_multi_level(row):
    dummy = MultiLevelNode(0)
    tail = dummy
    for value, child_row in row:
        tail.next = MultiLevelNode(value)
        tail = tail.next
        if child_row:
            tail.child = _build_multi_level(child_row)
    return dummy.next


def _flatten_by_levels_brute(row):
    result, level = [], [row]
    while level:
        next_level = []
        for current_row in level:
            for value, child_row in current_row:
                result.append(value)
                if child_row:
                    next_level.append(child_row)
        level = next_level
    return result


def _flatten_depth_first_brute(row):
    result = []
    for value, child_row in row:
        result.append(value)
        if child_row:
            result.extend(_flatten_depth_first_brute(child_row))
    return result


def _random_row(depth):
    row = []
    for _ in range(RNG.randint(1, 4)):
        child_row = _random_row(depth + 1) if depth < 3 and RNG.random() < 0.4 else None
        row.append((RNG.randint(0, 99), child_row))
    return row


# 1 → 2 → 3 → 4
#     |       |
#     5 → 6   7
#     |
#     8 → 9
SAMPLE_ROW = [
    (1, None),
    (2, [(5, [(8, None), (9, None)]), (6, None)]),
    (3, None),
    (4, [(7, None)]),
]


def test_flatten_examples():
    head = flatten_multi_level_list(_build_multi_level(SAMPLE_ROW))
    assert to_values(head) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert all(node.child is None for node in iter_nodes(head))

    head = flatten_multi_level_list_depth_first(_build_multi_level(SAMPLE_ROW))
    assert to_values(head) == [1, 2, 5, 8, 9, 6, 3, 4, 7]
    assert all(node.child is None for node in iter_nodes(head))


@pytest.mark.parametrize(
    "flatten", [flatten_multi_level_list, flatten_multi_level_list_depth_first]
)
def test_flatten_edge_cases(flatten):
    assert flatten(None) is None
    assert to_values(flatten(_build_multi_level([(1, None), (2, None)]))) == [1, 2]
    # Цепочка из одних child: каждый уровень — один узел.
    chain = [(1, [(2, [(3, [(4, None)])])])]
    assert to_values(flatten(_build_multi_level(chain))) == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "flatten, brute",
    [
        (flatten_multi_level_list, _flatten_by_levels_brute),
        (flatten_multi_level_list_depth_first, _flatten_depth_first_brute),
    ],
)
def test_flatten_random(flatten, brute):
    for _ in range(ROUNDS):
        row = _random_row(0)
        head = _build_multi_level(row)
        total = len(brute(row))
        result = flatten(head)
        assert result is head
        assert to_values(result) == brute(row)
        nodes = list(iter_nodes(result))
        assert len(nodes) == total
        assert all(node.child is None for node in nodes)

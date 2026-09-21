"""Тесты к паттерну Fast and Slow Pointers.

Кроме ручных примеров каждое решение сверяется с очевидно правильным
эталоном на случайных данных: эталон тратит O(n) памяти (запоминает
пройденные узлы или числа), зато ошибиться в нём негде.
"""

import random

import pytest

from fast_and_slow_pointers_helpers import build_list
from happy_number import happy_number
from linked_list_loop import linked_list_loop, linked_list_loop_start
from linked_list_midpoint import linked_list_midpoint, linked_list_midpoint_first

RNG = random.Random(2024)
ROUNDS = 500


def _random_list():
    """Случайный список: (голова, длина, индекс входа в цикл или None)."""
    length = RNG.randint(0, 12)
    # Значения нарочно повторяются: решение обязано сравнивать узлы, а не числа.
    values = [RNG.randint(0, 3) for _ in range(length)]
    loop_to = RNG.randrange(length) if length and RNG.random() < 0.6 else None
    return build_list(values, loop_to), length, loop_to


# ---------- helpers ----------

def test_build_list():
    assert build_list([]) is None

    head = build_list([1, 2, 3])
    assert [head.val, head.next.val, head.next.next.val] == [1, 2, 3]
    assert head.next.next.next is None

    looped = build_list([1, 2, 3], loop_to=1)
    assert looped.next.next.next is looped.next

    with pytest.raises(ValueError):
        build_list([1, 2], loop_to=2)
    with pytest.raises(ValueError):
        build_list([], loop_to=0)


# ---------- linked_list_loop ----------

def _loop_start_brute(head):
    """Первый узел, в который мы пришли повторно; None — если дошли до конца."""
    visited = set()
    node = head
    while node is not None:
        if id(node) in visited:
            return node
        visited.add(id(node))
        node = node.next
    return None


def test_linked_list_loop_examples():
    assert linked_list_loop(build_list([4, 8, 15, 16, 23, 42], loop_to=2))
    assert not linked_list_loop(build_list([4, 8, 15, 16, 23, 42]))
    assert not linked_list_loop(None)
    assert not linked_list_loop(build_list([7]))
    assert linked_list_loop(build_list([7], loop_to=0))         # узел замкнут на себя
    assert not linked_list_loop(build_list([7, 7]))
    assert linked_list_loop(build_list([7, 7], loop_to=0))
    assert linked_list_loop(build_list([1, 2, 3, 4], loop_to=3))   # петля на хвосте
    # Одинаковые значения без цикла: сравнение по значению дало бы ложный True.
    assert not linked_list_loop(build_list([5, 5, 5, 5, 5, 5]))


def test_linked_list_loop_start_examples():
    head = build_list([4, 8, 15, 16, 23, 42], loop_to=2)
    start = linked_list_loop_start(head)
    assert start is head.next.next and start.val == 15

    whole = build_list([1, 2, 3], loop_to=0)            # весь список — кольцо
    assert linked_list_loop_start(whole) is whole

    # Длинный хвост и короткий цикл: быстрый успевает намотать много кругов.
    long_tail = build_list(list(range(10)), loop_to=8)
    assert linked_list_loop_start(long_tail).val == 8

    self_loop = build_list([1, 2, 3], loop_to=2)
    assert linked_list_loop_start(self_loop).val == 3

    assert linked_list_loop_start(build_list([1, 2, 3])) is None
    assert linked_list_loop_start(None) is None


def test_linked_list_loop_random():
    for _ in range(ROUNDS):
        head, _, loop_to = _random_list()
        expected = _loop_start_brute(head)
        assert (expected is None) == (loop_to is None)     # эталон согласен с генератором
        assert linked_list_loop(head) == (expected is not None)
        assert linked_list_loop_start(head) is expected


def test_linked_list_loop_does_not_modify_list():
    head = build_list([1, 2, 3, 4, 5], loop_to=1)
    nodes = [head]
    for _ in range(4):
        nodes.append(nodes[-1].next)
    linked_list_loop(head)
    linked_list_loop_start(head)
    assert [node.val for node in nodes] == [1, 2, 3, 4, 5]
    assert all(a.next is b for a, b in zip(nodes, nodes[1:]))
    assert nodes[-1].next is nodes[1]


def test_linked_list_loop_is_linear_on_long_list():
    size = 200_000
    assert not linked_list_loop(build_list(range(size)))
    assert linked_list_loop_start(build_list(range(size), loop_to=size // 2)).val == size // 2


# ---------- linked_list_midpoint ----------

def _nodes_brute(head):
    nodes = []
    while head is not None:
        nodes.append(head)
        head = head.next
    return nodes


def test_linked_list_midpoint_examples():
    assert linked_list_midpoint(build_list([3, 1, 4, 1, 5])).val == 4
    assert linked_list_midpoint(build_list([2, 7, 1, 8, 2, 9])).val == 8    # второй из двух
    assert linked_list_midpoint(build_list([6])).val == 6
    assert linked_list_midpoint(build_list([6, 9])).val == 9
    assert linked_list_midpoint(None) is None


def test_linked_list_midpoint_first_examples():
    assert linked_list_midpoint_first(build_list([3, 1, 4, 1, 5])).val == 4
    assert linked_list_midpoint_first(build_list([2, 7, 1, 8, 2, 9])).val == 1  # первый из двух
    assert linked_list_midpoint_first(build_list([6])).val == 6
    assert linked_list_midpoint_first(build_list([6, 9])).val == 6
    assert linked_list_midpoint_first(None) is None


def test_linked_list_midpoint_random():
    for _ in range(ROUNDS):
        length = RNG.randint(0, 15)
        head = build_list([RNG.randint(0, 3) for _ in range(length)])
        nodes = _nodes_brute(head)
        if not nodes:
            assert linked_list_midpoint(head) is None
            assert linked_list_midpoint_first(head) is None
            continue
        # Сверяем сами узлы, а не значения: значения повторяются.
        assert linked_list_midpoint(head) is nodes[len(nodes) // 2]
        assert linked_list_midpoint_first(head) is nodes[(len(nodes) - 1) // 2]


# ---------- happy_number ----------

def _happy_brute(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return n == 1


def test_happy_number_examples():
    assert happy_number(1)
    assert happy_number(23)             # 23 -> 13 -> 10 -> 1
    assert not happy_number(24)
    assert not happy_number(2)
    assert not happy_number(4)          # 4 лежит прямо на «несчастливом» цикле
    assert happy_number(7)
    assert happy_number(10 ** 30)       # цифры: единица и нули
    assert not happy_number(10 ** 30 + 1)


def test_happy_number_first_hundred():
    # Известный ряд счастливых чисел (OEIS A007770).
    expected = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100]
    assert [n for n in range(1, 101) if happy_number(n)] == expected


def test_happy_number_rejects_non_positive():
    for bad in (0, -7):
        with pytest.raises(ValueError):
            happy_number(bad)


def test_happy_number_random():
    for _ in range(ROUNDS):
        n = RNG.randint(1, 10 ** RNG.randint(1, 18))
        assert happy_number(n) == _happy_brute(n)

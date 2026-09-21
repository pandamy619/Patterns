"""Тесты к паттерну Two Pointers.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор медленный, зато очевидно правильный.
"""

import random
from itertools import combinations, permutations

from is_palindrome_valid import is_palindrome_valid
from largest_container import largest_container
from next_lexicographical_sequence import next_lexicographical_sequence
from pair_sum_sorted import pair_sum_sorted
from shift_zeros_to_end import shift_zeros_to_end
from triplet_sum import triplet_sum

RNG = random.Random(2024)
ROUNDS = 500


# ---------- pair_sum_sorted ----------

def test_pair_sum_sorted_examples():
    assert pair_sum_sorted([-7, -1, 2, 5, 9], 4) == [1, 3]
    assert pair_sum_sorted([3, 3], 6) == [0, 1]
    assert pair_sum_sorted([1, 2, 4], 100) == []
    assert pair_sum_sorted([], 0) == []
    assert pair_sum_sorted([5], 5) == []


def test_pair_sum_sorted_random():
    for _ in range(ROUNDS):
        nums = sorted(RNG.randint(-10, 10) for _ in range(RNG.randint(0, 8)))
        target = RNG.randint(-20, 20)
        exists = any(a + b == target for a, b in combinations(nums, 2))
        answer = pair_sum_sorted(nums, target)
        if exists:
            i, j = answer
            assert i != j and nums[i] + nums[j] == target
        else:
            assert answer == []


# ---------- triplet_sum ----------

def _triplets_brute(nums):
    return {tuple(sorted(t)) for t in combinations(nums, 3) if sum(t) == 0}


def test_triplet_sum_examples():
    assert triplet_sum([4, -6, 2, 0, -2, 2]) == [[-6, 2, 4], [-2, 0, 2]]
    assert triplet_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert triplet_sum([1, 2, 3]) == []
    assert triplet_sum([]) == []
    assert triplet_sum([0, 0]) == []


def test_triplet_sum_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-5, 5) for _ in range(RNG.randint(0, 9))]
        answer = triplet_sum(nums)
        as_tuples = [tuple(sorted(t)) for t in answer]
        assert len(as_tuples) == len(set(as_tuples)), "в ответе есть дубликаты"
        assert set(as_tuples) == _triplets_brute(nums)


def test_triplet_sum_does_not_mutate_input():
    nums = [3, -1, -2, 0]
    triplet_sum(nums)
    assert nums == [3, -1, -2, 0]


# ---------- is_palindrome_valid ----------

def test_is_palindrome_valid_examples():
    assert is_palindrome_valid("А роза упала на лапу Азора")
    assert is_palindrome_valid("No lemon, no melon!")
    assert is_palindrome_valid("12:21")
    assert is_palindrome_valid("")
    assert is_palindrome_valid("?!..")
    assert not is_palindrome_valid("two pointers")
    assert not is_palindrome_valid("1a2")


def test_is_palindrome_valid_random():
    alphabet = "abAB12 ,!"
    for _ in range(ROUNDS):
        text = "".join(RNG.choice(alphabet) for _ in range(RNG.randint(0, 10)))
        cleaned = [c.lower() for c in text if c.isalnum()]
        assert is_palindrome_valid(text) == (cleaned == cleaned[::-1])


# ---------- largest_container ----------

def test_largest_container_examples():
    assert largest_container([3, 9, 4, 1, 8, 2]) == 24
    assert largest_container([5, 5]) == 5
    assert largest_container([0, 0, 0]) == 0
    assert largest_container([7]) == 0
    assert largest_container([]) == 0


def test_largest_container_random():
    for _ in range(ROUNDS):
        heights = [RNG.randint(0, 12) for _ in range(RNG.randint(0, 9))]
        brute = max(
            (min(heights[i], heights[j]) * (j - i)
             for i, j in combinations(range(len(heights)), 2)),
            default=0,
        )
        assert largest_container(heights) == brute


# ---------- shift_zeros_to_end ----------

def test_shift_zeros_to_end_examples():
    nums = [0, 4, 0, 0, -3, 7]
    shift_zeros_to_end(nums)
    assert nums == [4, -3, 7, 0, 0, 0]

    for case in ([], [0], [1], [0, 0], [1, 2, 3]):
        nums = list(case)
        shift_zeros_to_end(nums)
        assert nums == [x for x in case if x] + [0] * case.count(0)


def test_shift_zeros_to_end_random():
    for _ in range(ROUNDS):
        original = [RNG.choice([0, 0, 1, 2, 3, -1]) for _ in range(RNG.randint(0, 10))]
        nums = list(original)
        shift_zeros_to_end(nums)
        assert nums == [x for x in original if x] + [0] * original.count(0)


# ---------- next_lexicographical_sequence ----------

def test_next_lexicographical_sequence_examples():
    assert next_lexicographical_sequence("abc") == "acb"
    assert next_lexicographical_sequence("bdca") == "cabd"
    assert next_lexicographical_sequence("cba") == "abc"   # последняя -> первая
    assert next_lexicographical_sequence("aab") == "aba"
    assert next_lexicographical_sequence("zz") == "zz"
    assert next_lexicographical_sequence("x") == "x"
    assert next_lexicographical_sequence("") == ""


def test_next_lexicographical_sequence_random():
    for _ in range(ROUNDS):
        text = "".join(RNG.choice("abcd") for _ in range(RNG.randint(1, 6)))
        ordered = sorted(set(permutations(text)))
        position = ordered.index(tuple(text))
        expected = "".join(ordered[(position + 1) % len(ordered)])
        assert next_lexicographical_sequence(text) == expected

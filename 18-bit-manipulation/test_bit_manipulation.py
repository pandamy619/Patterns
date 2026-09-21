"""Тесты к паттерну Bit Manipulation.

Кроме ручных примеров каждое решение сверяется с очевидно правильным
эталоном на случайных данных: строковое представление bin(x), Counter,
перестановка символов в двоичной строке.
"""

import random
from collections import Counter

import pytest

from hamming_weights_of_integers import (
    count_set_bits,
    count_set_bits_kernighan,
    hamming_weights_bit_by_bit,
    hamming_weights_of_integers,
)
from lonely_integer import lonely_integer
from swap_odd_and_even_bits import (
    EVEN_MASK,
    ODD_MASK,
    UINT32_MASK,
    swap_odd_and_even_bits,
    swap_odd_and_even_bits_naive,
)

RNG = random.Random(2024)
ROUNDS = 500


# ---------- hamming_weights_of_integers ----------

def _weights_brute(n):
    return [bin(x).count("1") for x in range(n + 1)]


def test_hamming_weights_examples():
    expected = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2]
    assert hamming_weights_of_integers(10) == expected
    assert hamming_weights_bit_by_bit(10) == expected
    assert hamming_weights_of_integers(0) == [0]
    assert hamming_weights_bit_by_bit(0) == [0]
    assert hamming_weights_of_integers(1) == [0, 1]


def test_hamming_weights_powers_of_two():
    weights = hamming_weights_of_integers(1024)
    for power in range(11):
        assert weights[1 << power] == 1              # одна единица
        if power:
            assert weights[(1 << power) - 1] == power  # сплошные единицы


def test_count_set_bits_examples():
    for counter in (count_set_bits, count_set_bits_kernighan):
        assert counter(0) == 0
        assert counter(0b101100) == 3
        assert counter(UINT32_MASK) == 32
        assert counter(1 << 100) == 1                # длинная арифметика
        with pytest.raises(ValueError):
            counter(-1)


def test_hamming_weights_reject_negative():
    with pytest.raises(ValueError):
        hamming_weights_of_integers(-1)
    with pytest.raises(ValueError):
        hamming_weights_bit_by_bit(-5)


def test_hamming_weights_random():
    for _ in range(ROUNDS):
        n = RNG.randint(0, 300)
        expected = _weights_brute(n)
        assert hamming_weights_of_integers(n) == expected
        assert hamming_weights_bit_by_bit(n) == expected


def test_count_set_bits_random():
    for _ in range(ROUNDS):
        x = RNG.getrandbits(RNG.randint(1, 80))
        expected = bin(x).count("1")
        assert count_set_bits(x) == expected
        assert count_set_bits_kernighan(x) == expected


# ---------- lonely_integer ----------

def _lonely_brute(nums):
    (value,) = [v for v, freq in Counter(nums).items() if freq == 1]
    return value


def test_lonely_integer_examples():
    assert lonely_integer([6, 9, 4, 9, 6]) == 4
    assert lonely_integer([42]) == 42
    assert lonely_integer([0, 5, 5]) == 0            # одиночка — ноль
    assert lonely_integer([-3, 8, -3]) == 8
    assert lonely_integer([8, -3, 8]) == -3          # отрицательная одиночка
    assert lonely_integer([7, 7, 2**40, 1, 1]) == 2**40


def test_lonely_integer_rejects_empty():
    with pytest.raises(ValueError):
        lonely_integer([])


def test_lonely_integer_random():
    for _ in range(ROUNDS):
        pool = RNG.sample(range(-50, 51), RNG.randint(1, 10))
        loner, paired = pool[0], pool[1:]
        nums = [loner] + paired * 2
        RNG.shuffle(nums)
        assert lonely_integer(nums) == loner == _lonely_brute(nums)


# ---------- swap_odd_and_even_bits ----------

def _swap_brute(n):
    """Эталон на строках: режем 32 символа на пары и разворачиваем каждую."""
    bits = format(n, "032b")
    pairs = [bits[i + 1] + bits[i] for i in range(0, 32, 2)]
    return int("".join(pairs), 2)


def test_swap_examples():
    assert swap_odd_and_even_bits(0b100110) == 0b011001      # 38 -> 25
    assert swap_odd_and_even_bits(0) == 0
    assert swap_odd_and_even_bits(1) == 2
    assert swap_odd_and_even_bits(2) == 1
    assert swap_odd_and_even_bits(0b11) == 0b11              # пара одинаковых
    assert swap_odd_and_even_bits(UINT32_MASK) == UINT32_MASK
    assert swap_odd_and_even_bits(EVEN_MASK) == ODD_MASK
    assert swap_odd_and_even_bits(ODD_MASK) == EVEN_MASK
    assert swap_odd_and_even_bits(1 << 31) == 1 << 30        # старший бит
    assert swap_odd_and_even_bits(1 << 30) == 1 << 31


def test_swap_masks_are_complementary():
    assert EVEN_MASK | ODD_MASK == UINT32_MASK
    assert EVEN_MASK & ODD_MASK == 0
    assert ~EVEN_MASK & UINT32_MASK == ODD_MASK              # ~ без маски даст минус


def test_swap_rejects_out_of_range():
    for bad in (-1, 1 << 32):
        with pytest.raises(ValueError):
            swap_odd_and_even_bits(bad)
        with pytest.raises(ValueError):
            swap_odd_and_even_bits_naive(bad)


def test_swap_random():
    for _ in range(ROUNDS):
        n = RNG.getrandbits(32)
        swapped = swap_odd_and_even_bits(n)
        assert swapped == _swap_brute(n) == swap_odd_and_even_bits_naive(n)
        assert 0 <= swapped <= UINT32_MASK
        assert swap_odd_and_even_bits(swapped) == n          # обмен обратим

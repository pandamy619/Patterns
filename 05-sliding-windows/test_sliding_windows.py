"""Тесты к паттерну Sliding Windows.

Кроме ручных примеров каждое решение сверяется с полным перебором
на случайных данных: перебор медленный, зато очевидно правильный.
"""

import random

import pytest

from longest_substring_with_unique_characters import (
    longest_substring_with_unique_characters,
    longest_substring_with_unique_characters_optimized,
)
from longest_uniform_substring_after_replacements import (
    longest_uniform_substring_after_replacements,
    longest_uniform_substring_after_replacements_shrinking,
)
from substring_anagrams import substring_anagrams

RNG = random.Random(2024)
ROUNDS = 500


def _random_string(alphabet: str, max_len: int) -> str:
    return "".join(RNG.choice(alphabet) for _ in range(RNG.randint(0, max_len)))


# ---------- substring_anagrams ----------

def _anagrams_brute(s, t):
    if not t:
        return 0
    target = sorted(t)
    return sum(
        1
        for start in range(len(s) - len(t) + 1)
        if sorted(s[start:start + len(t)]) == target
    )


def test_substring_anagrams_examples():
    assert substring_anagrams("tropotpor", "opt") == 3
    assert substring_anagrams("aaaa", "aa") == 3          # окна пересекаются
    assert substring_anagrams("abab", "ab") == 3          # "ab", "ba", "ab"
    assert substring_anagrams("listen", "silent") == 1    # окно во всю строку
    assert substring_anagrams("abc", "abd") == 0
    assert substring_anagrams("aab", "abb") == 0          # буквы те же, частоты нет
    assert substring_anagrams("ab", "abc") == 0           # t длиннее s
    assert substring_anagrams("", "a") == 0
    assert substring_anagrams("abc", "") == 0
    assert substring_anagrams("z", "z") == 1


def test_substring_anagrams_random():
    for _ in range(ROUNDS):
        s = _random_string("abc", 12)
        t = _random_string("abc", 4)
        assert substring_anagrams(s, t) == _anagrams_brute(s, t)


def test_substring_anagrams_does_not_depend_on_alphabet():
    # Символы вне латиницы и длинный вход: таблица на 26 ячеек тут бы упала.
    s = "кот ток окт" * 20_000
    assert substring_anagrams(s, "ток") == _anagrams_brute(s, "ток")


# ---------- longest_substring_with_unique_characters ----------

UNIQUE_SOLUTIONS = [
    longest_substring_with_unique_characters,
    longest_substring_with_unique_characters_optimized,
]


def _unique_brute(s):
    return max(
        (
            end - start
            for start in range(len(s))
            for end in range(start + 1, len(s) + 1)
            if len(set(s[start:end])) == end - start
        ),
        default=0,
    )


@pytest.mark.parametrize("solve", UNIQUE_SOLUTIONS)
def test_longest_unique_examples(solve):
    assert solve("moloko") == 3               # "mol" или "lok"
    assert solve("kabak") == 3                # "kab" или "bak"
    assert solve("abcdef") == 6               # вся строка
    assert solve("zzzz") == 1
    assert solve("abba") == 2                 # устаревшая позиция 'a' левее окна
    assert solve("q") == 1
    assert solve("") == 0
    assert solve("a a") == 2                  # пробел — такой же символ


@pytest.mark.parametrize("solve", UNIQUE_SOLUTIONS)
def test_longest_unique_random(solve):
    for _ in range(ROUNDS):
        s = _random_string("abcd", 14)
        assert solve(s) == _unique_brute(s)


@pytest.mark.parametrize("solve", UNIQUE_SOLUTIONS)
def test_longest_unique_is_linear(solve):
    s = "abcdefghij" * 50_000
    assert solve(s) == 10


# ---------- longest_uniform_substring_after_replacements ----------

UNIFORM_SOLUTIONS = [
    longest_uniform_substring_after_replacements,
    longest_uniform_substring_after_replacements_shrinking,
]


def _uniform_brute(s, k):
    best = 0
    for start in range(len(s)):
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            most_common = max(piece.count(ch) for ch in set(piece))
            if len(piece) - most_common <= k:
                best = max(best, len(piece))
    return best


@pytest.mark.parametrize("solve", UNIFORM_SOLUTIONS)
def test_longest_uniform_examples(solve):
    assert solve("xxyzxxwx", 2) == 6          # "xxyzxx" -> "xxxxxx"
    assert solve("xxyzxxwx", 0) == 2          # без замен — просто самая длинная серия
    assert solve("abcd", 1) == 2
    assert solve("abcd", 10) == 4             # k больше длины строки
    assert solve("pppp", 2) == 4              # менять нечего
    assert solve("abab", 2) == 4
    assert solve("a", 0) == 1
    assert solve("", 3) == 0


@pytest.mark.parametrize("solve", UNIFORM_SOLUTIONS)
def test_longest_uniform_rejects_negative_k(solve):
    with pytest.raises(ValueError):
        solve("abc", -1)


@pytest.mark.parametrize("solve", UNIFORM_SOLUTIONS)
def test_longest_uniform_random(solve):
    for _ in range(ROUNDS):
        s = _random_string("abc", 12)
        k = RNG.randint(0, 4)
        assert solve(s, k) == _uniform_brute(s, k)


def test_longest_uniform_is_linear():
    s = "ab" * 250_000
    assert longest_uniform_substring_after_replacements(s, 1000) == 2001

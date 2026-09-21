"""Самая длинная подстрока из одинаковых символов после не более чем k замен.

Приём: dynamic window (окно переменной длины). Основной вариант окно
не сжимает вовсе: оно либо растёт, либо сдвигается с той же длиной.
Для сравнения рядом лежит классический вариант со сжатием.
Аналог: LeetCode 424.
"""

from collections import defaultdict


def longest_uniform_substring_after_replacements(s: str, k: int) -> int:
    """Окно, которое никогда не уменьшается.

    Время O(n), память O(|алфавит|).
    """
    if k < 0:
        raise ValueError("k не может быть отрицательным")

    counts: defaultdict[str, int] = defaultdict(int)
    # Наибольшая частота одного символа, которая КОГДА-ЛИБО встречалась
    # в окне. При сдвиге не уменьшается — и это сделано намеренно:
    # побить рекорд длины может только окно с большей частотой, а меньшая
    # частота рекорду ничем не поможет.
    top_count = 0
    left = 0

    for right, ch in enumerate(s):
        counts[ch] += 1
        # Вырасти могла только частота вошедшего символа,
        # поэтому не нужно искать максимум по всей таблице.
        top_count = max(top_count, counts[ch])

        # Замен требуется «длина окна минус самый частый символ».
        # Не хватает — сдвигаем окно целиком: if, а не while. Окно выросло
        # на один символ, значит одного шага левой границы достаточно,
        # чтобы вернуться к прежней, заведомо допустимой длине.
        if (right - left + 1) - top_count > k:
            counts[s[left]] -= 1
            left += 1

    # Длина окна не убывала и росла только до достижимых значений,
    # так что последнее окно и есть рекорд.
    return len(s) - left


def longest_uniform_substring_after_replacements_shrinking(s: str, k: int) -> int:
    """Классический вариант: окно честно сжимается, пока не станет допустимым,
    а наибольшая частота каждый раз пересчитывается по таблице.

    Время O(n * |алфавит|), память O(|алфавит|).
    """
    if k < 0:
        raise ValueError("k не может быть отрицательным")

    counts: defaultdict[str, int] = defaultdict(int)
    left = 0
    longest = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        while (right - left + 1) - max(counts.values()) > k:
            counts[s[left]] -= 1
            left += 1
        longest = max(longest, right - left + 1)
    return longest

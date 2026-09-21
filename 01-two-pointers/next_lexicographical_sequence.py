"""Следующая в лексикографическом порядке перестановка символов строки.

Стратегия: staged traversal (поэтапное движение).
Аналог: LeetCode 31 (там массив чисел).
"""


def next_lexicographical_sequence(text: str) -> str:
    """Вернуть следующую перестановку; для последней — самую первую.

    Время O(n), память O(n) на список символов (строки в Python неизменяемы).
    """
    chars = list(text)
    n = len(chars)

    # Этап 1. Идём справа, ищем «точку перелома» — первый символ,
    # который меньше своего правого соседа. Хвост после неё не возрастает.
    pivot = n - 2
    while pivot >= 0 and chars[pivot] >= chars[pivot + 1]:
        pivot -= 1

    if pivot >= 0:
        # Этап 2. Второй указатель ищет в хвосте самый правый символ,
        # который больше chars[pivot], — это минимально возможная замена.
        successor = n - 1
        while chars[successor] <= chars[pivot]:
            successor -= 1
        chars[pivot], chars[successor] = chars[successor], chars[pivot]

    # Хвост по-прежнему не возрастает; разворот делает его минимальным.
    # При pivot == -1 разворачивается вся строка — получаем первую перестановку.
    chars[pivot + 1:] = reversed(chars[pivot + 1:])
    return "".join(chars)

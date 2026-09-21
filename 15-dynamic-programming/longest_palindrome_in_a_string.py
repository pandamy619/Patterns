"""Самая длинная палиндромная подстрока.

Два решения: DP по отрезкам (таблица «отрезок [i..j] — палиндром?»)
и расширение от центра, которому таблица не нужна.
При нескольких ответах одинаковой длины оба возвращают самый левый.
Аналог: LeetCode 5.
"""


def longest_palindrome_in_a_string_table(text: str) -> str:
    """DP по отрезкам: от коротких подстрок к длинным.

    Время O(n^2), память O(n^2).
    """
    size = len(text)
    if size == 0:
        return ""
    # База: любой одиночный символ — палиндром.
    is_pal = [[False] * size for _ in range(size)]
    for i in range(size):
        is_pal[i][i] = True
    best_start, best_length = 0, 1

    # Отрезок [i..j] зависит от [i+1..j-1], который короче на 2. Поэтому внешний
    # цикл — по ДЛИНЕ: когда доходим до длины L, все более короткие уже готовы.
    # Цикл «по i, потом по j» слева направо читал бы ещё не заполненные клетки.
    for length in range(2, size + 1):
        for start in range(size - length + 1):
            end = start + length - 1
            if text[start] != text[end]:
                continue
            # Для длины 2 внутри ничего нет — пустая середина считается палиндромом.
            if length == 2 or is_pal[start + 1][end - 1]:
                is_pal[start][end] = True
                if length > best_length:
                    best_start, best_length = start, length
    return text[best_start:best_start + best_length]


def longest_palindrome_in_a_string(text: str) -> str:
    """Расширение от центра: у строки 2n - 1 центров, от каждого растём в стороны.

    Время O(n^2), память O(1).
    """
    size = len(text)
    best_start, best_length = 0, 0

    def expand(left: int, right: int) -> tuple[int, int]:
        """Растягивает палиндром, пока края совпадают; возвращает (начало, длина)."""
        while left >= 0 and right < size and text[left] == text[right]:
            left -= 1
            right += 1
        # Цикл остановился на шаг ПОЗЖЕ, чем нужно: границы уже «испорчены».
        return left + 1, right - left - 1

    for center in range(size):
        # Центр-символ даёт палиндромы нечётной длины,
        # центр-промежуток между center и center + 1 — чётной.
        for start, length in (expand(center, center), expand(center, center + 1)):
            if length > best_length:
                best_start, best_length = start, length
    return text[best_start:best_start + best_length]

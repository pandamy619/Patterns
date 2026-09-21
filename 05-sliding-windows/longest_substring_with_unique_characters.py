"""Длина самой длинной подстроки без повторяющихся символов.

Приём: dynamic window (окно переменной длины). Два варианта:
множество символов окна и хеш-таблица последних позиций,
которая позволяет левой границе прыгать, а не ползти.
Аналог: LeetCode 3.
"""


def longest_substring_with_unique_characters(s: str) -> int:
    """Вариант с множеством: при повторе сжимаем окно по одному символу.

    Время O(n): каждый символ один раз входит в окно и не более одного
    раза выходит. Память O(min(n, |алфавит|)).
    """
    window: set[str] = set()
    left = 0
    longest = 0
    for right, ch in enumerate(s):
        # Дубликат может быть только один — сам ch. Выбрасываем символы
        # слева, пока не выбросим его прежнее вхождение.
        while ch in window:
            window.remove(s[left])
            left += 1
        window.add(ch)
        longest = max(longest, right - left + 1)
    return longest


def longest_substring_with_unique_characters_optimized(s: str) -> int:
    """Вариант с таблицей последних позиций: левая граница прыгает сразу
    за прежнее вхождение повторившегося символа.

    Время O(n) — ровно один проход, без внутреннего цикла.
    Память O(min(n, |алфавит|)).
    """
    last_seen: dict[str, int] = {}  # символ -> индекс его последнего вхождения
    left = 0
    longest = 0
    for right, ch in enumerate(s):
        # Записи из таблицы не удаляются, поэтому в ней остаются и символы,
        # которые уже левее окна. Сравнение с left отсеивает такие
        # «устаревшие» позиции — иначе граница уехала бы назад.
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        longest = max(longest, right - left + 1)
    return longest

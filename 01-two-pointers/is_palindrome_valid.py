"""Палиндром с учётом только букв и цифр, без учёта регистра.

Стратегия: inward traversal (встречное движение).
Аналог: LeetCode 125.
"""


def is_palindrome_valid(text: str) -> bool:
    """True, если буквы и цифры строки читаются одинаково в обе стороны.

    Время O(n), память O(1) — строка не копируется и не очищается заранее.
    """
    lo, hi = 0, len(text) - 1
    while lo < hi:
        if not text[lo].isalnum():
            lo += 1
        elif not text[hi].isalnum():
            hi -= 1
        elif text[lo].lower() != text[hi].lower():
            return False
        else:
            lo += 1
            hi -= 1
    return True

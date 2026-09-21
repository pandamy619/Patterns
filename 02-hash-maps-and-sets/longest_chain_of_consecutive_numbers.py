"""Длина самой длинной цепочки последовательных чисел.

Идея: множество для проверки за O(1) и запуск подсчёта только
с НАЧАЛА цепочки.
Аналог: LeetCode 128.
"""


def longest_chain_of_consecutive_numbers(nums: list[int]) -> int:
    """Наибольшее k, для которого в nums есть x, x+1, ..., x+k-1.
    Порядок в массиве не важен, дубликаты не учитываются.

    Время O(n), память O(n).
    """
    values = set(nums)
    longest = 0
    for value in values:
        # Если есть value - 1, то value — не начало: эту цепочку
        # посчитаем (или уже посчитали) от её настоящего начала.
        if value - 1 in values:
            continue
        length = 1
        while value + length in values:
            length += 1
        longest = max(longest, length)
    return longest

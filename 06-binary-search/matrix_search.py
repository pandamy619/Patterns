"""Поиск числа в матрице, строки которой продолжают друг друга по возрастанию.

Приём: exact match (поиск точного совпадения) по «виртуальному» одномерному
массиву: индекс i соответствует клетке (i // cols, i % cols).
Аналог: LeetCode 74.
"""


def matrix_search(matrix: list[list[int]], target: int) -> bool:
    """Есть ли target в матрице.

    Время O(log(m·n)), память O(1).
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    # Если выписать строки одну за другой, получится один отсортированный
    # массив длиной rows * cols. Склеивать его на самом деле не нужно —
    # достаточно уметь переводить номер элемента в координаты.
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

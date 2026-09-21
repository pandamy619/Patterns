"""Обнулить строку и столбец каждой клетки, где изначально стоял ноль.

Два решения: с множествами (память O(m + n)) и с метками прямо
в первой строке и первом столбце (память O(1)).
Аналог: LeetCode 73.
"""


def zero_striping(matrix: list[list[int]]) -> None:
    """Вариант с множествами. Изменяет matrix на месте.

    Время O(m * n), память O(m + n).
    """
    if not matrix or not matrix[0]:
        return
    zero_rows: set[int] = set()
    zero_cols: set[int] = set()

    # Проход 1: только запоминаем. Обнулять сразу нельзя — новые нули
    # неотличимы от исходных и «заразят» всю матрицу.
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0:
                zero_rows.add(r)
                zero_cols.add(c)

    # Проход 2: обнуляем.
    for r, row in enumerate(matrix):
        for c in range(len(row)):
            if r in zero_rows or c in zero_cols:
                row[c] = 0


def zero_striping_in_place(matrix: list[list[int]]) -> None:
    """Вариант без дополнительной памяти: роль множеств играют
    первая строка и первый столбец самой матрицы.

    Время O(m * n), память O(1).
    """
    if not matrix or not matrix[0]:
        return
    m, n = len(matrix), len(matrix[0])

    # Первая строка и столбец сейчас станут «блокнотом» и затрутся метками,
    # поэтому их собственное состояние запоминаем заранее.
    first_row_has_zero = any(matrix[0][c] == 0 for c in range(n))
    first_col_has_zero = any(matrix[r][0] == 0 for r in range(m))

    # Метки: ноль в клетке (r, c) -> ноль в начале строки r и столбца c.
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Обнуляем внутреннюю часть по меткам.
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    # Сам «блокнот» — в последнюю очередь, иначе испортим метки.
    if first_row_has_zero:
        for c in range(n):
            matrix[0][c] = 0
    if first_col_has_zero:
        for r in range(m):
            matrix[r][0] = 0

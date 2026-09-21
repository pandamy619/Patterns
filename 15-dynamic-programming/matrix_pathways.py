"""Число маршрутов из левого верхнего угла сетки в правый нижний (ходы: вправо, вниз).

Приём: 2D DP по сетке, затем сжатие таблицы до одной строки.
Аналог: LeetCode 62.
"""

from math import comb


def _check(rows: int, cols: int) -> None:
    if rows < 1 or cols < 1:
        raise ValueError("в сетке должна быть хотя бы одна клетка")


def matrix_pathways_grid(rows: int, cols: int) -> int:
    """Полная таблица: paths[r][c] — сколько маршрутов ведёт в клетку (r, c).

    Время O(rows * cols), память O(rows * cols).
    """
    _check(rows, cols)
    # Первая строка и первый столбец — база: туда ведёт единственная
    # прямая дорога. Поэтому таблицу сразу заполняем единицами.
    paths = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            # В клетку входят либо сверху, либо слева — третьего не дано.
            paths[r][c] = paths[r - 1][c] + paths[r][c - 1]
    return paths[-1][-1]


def matrix_pathways(rows: int, cols: int) -> int:
    """Одна строка вместо таблицы.

    Время O(rows * cols), память O(min(rows, cols)).
    """
    _check(rows, cols)
    # Задача симметрична, так что строку выгодно вести вдоль короткой стороны.
    if cols > rows:
        rows, cols = cols, rows
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            # До присваивания row[c] хранит значение «сверху» (прошлая строка),
            # а row[c - 1] уже обновлён — это значение «слева».
            row[c] += row[c - 1]
    return row[-1]


def matrix_pathways_formula(rows: int, cols: int) -> int:
    """Комбинаторика: из rows + cols - 2 ходов выбираем, какие будут «вниз».

    Время O(min(rows, cols)) умножений, память O(1). В тестах служит
    независимой проверкой.
    """
    _check(rows, cols)
    return comb(rows + cols - 2, rows - 1)

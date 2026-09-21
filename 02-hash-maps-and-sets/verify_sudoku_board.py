"""Проверка частично заполненного поля судоку.

Идея: по одному множеству на каждую строку, столбец и квадрат 3x3.
Аналог: LeetCode 36 (там пустая клетка — '.', здесь — 0).
"""

SIZE = 9
BOX = 3


def verify_sudoku_board(board: list[list[int]]) -> bool:
    """True, если ни одна цифра 1–9 не повторяется в строке, столбце
    или квадрате 3x3. Нули — пустые клетки. Решаемость НЕ проверяется.

    Время O(n^2), память O(n^2) для поля n x n (для 9x9 — константы).
    """
    rows = [set() for _ in range(SIZE)]
    cols = [set() for _ in range(SIZE)]
    boxes = [[set() for _ in range(BOX)] for _ in range(BOX)]

    for r in range(SIZE):
        for c in range(SIZE):
            digit = board[r][c]
            if digit == 0:
                continue
            box = boxes[r // BOX][c // BOX]
            if digit in rows[r] or digit in cols[c] or digit in box:
                return False
            rows[r].add(digit)
            cols[c].add(digit)
            box.add(digit)
    return True

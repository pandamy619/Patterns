"""N ферзей: сколько способов расставить n ферзей на доске n×n без боя.

Приём: choose → explore → unchoose плюс pruning. Ставим по одному ферзю
в строку, а занятые столбцы и диагонали держим в трёх множествах, чтобы
проверять клетку за O(1) и сразу отсекать битые ветки.
Аналог: LeetCode 52.
"""


def n_queens(n: int) -> int:
    """Число расстановок n ферзей на доске n×n, где никто никого не бьёт.

    Для n = 0 ответ 1: пустая доска, пустая расстановка.

    Время O(n!) — грубая верхняя оценка: в первой строке n вариантов,
    во второй не больше n − 1 и так далее; отсечения по диагоналям делают
    реальное дерево намного меньше. Память O(n).
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    busy_columns: set[int] = set()
    busy_diagonals: set[int] = set()       # «\»: на ней постоянна разность row - col
    busy_antidiagonals: set[int] = set()   # «/»: на ней постоянна сумма row + col

    def place(row: int) -> int:
        if row == n:
            return 1  # дошли до конца — значит, все n ферзей стоят мирно
        found = 0
        for col in range(n):
            # Строку проверять не нужно: в каждой строке ровно один ферзь
            # по построению.
            if (
                col in busy_columns
                or row - col in busy_diagonals
                or row + col in busy_antidiagonals
            ):
                continue  # отсечение: под этой клеткой решений нет
            busy_columns.add(col)
            busy_diagonals.add(row - col)
            busy_antidiagonals.add(row + col)
            found += place(row + 1)
            busy_columns.remove(col)
            busy_diagonals.remove(row - col)
            busy_antidiagonals.remove(row + col)
        return found

    return place(0)

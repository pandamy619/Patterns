"""Сколько островов в матрице из нулей (вода) и единиц (суша).

Приём: DFS (обход в глубину) по неявному графу на сетке — каждая найденная
клетка суши «заливается» вместе со всем своим островом.
Аналог: LeetCode 200.
"""

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def count_islands(matrix: list[list[int]]) -> int:
    """Число компонент связности из единиц (соседи — по четырём сторонам).

    Время O(m * n), память O(m * n) под отметки и стек.
    """
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    # Отдельная таблица отметок вместо затирания единиц: вход остаётся целым.
    # Если портить матрицу допустимо, память под отметки не нужна.
    visited = [[False] * cols for _ in range(rows)]

    def flood(start_r: int, start_c: int) -> None:
        # Явный стек вместо рекурсии: остров-«змейка» на поле 1000 x 1000
        # даёт глубину в сотни тысяч вызовов, рекурсия в Python столько не выдержит.
        stack = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            r, c = stack.pop()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and matrix[nr][nc] == 1
                    and not visited[nr][nc]
                ):
                    # Отмечаем при добавлении в стек, а не при извлечении,
                    # иначе одна клетка попадёт в стек несколько раз.
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 1 and not visited[r][c]:
                # Непосещённая суша — гарантированно новый остров:
                # все клетки прежних островов уже отмечены.
                islands += 1
                flood(r, c)
    return islands

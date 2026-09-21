"""Длина самого длинного строго возрастающего пути в матрице.

Ходить можно по четырём сторонам, каждая следующая клетка строго больше.
Приём: DFS с мемоизацией — рёбра «меньшее -> большее» образуют DAG,
поэтому ответ для клетки не зависит от того, как мы в неё пришли.
Аналог: LeetCode 329.
"""

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """DFS с мемоизацией.

    Время O(m * n): каждая клетка считается один раз, у неё не больше 4 рёбер.
    Память O(m * n) под таблицу и стек рекурсии.
    """
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    # best[r][c] — длина лучшего пути, НАЧИНАЮЩЕГОСЯ в клетке; 0 = ещё не считали.
    best = [[0] * cols for _ in range(rows)]

    def longest_from(r: int, c: int) -> int:
        if best[r][c]:
            return best[r][c]
        length = 1                      # сама клетка — уже путь
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            # Множество visited не нужно: строгое возрастание само
            # запрещает вернуться в уже пройденную клетку.
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                length = max(length, 1 + longest_from(nr, nc))
        best[r][c] = length
        return length

    return max(longest_from(r, c) for r in range(rows) for c in range(cols))


def longest_increasing_path_iterative(matrix: list[list[int]]) -> int:
    """Тот же ответ без рекурсии: клетки обрабатываются по убыванию значения.

    К моменту обработки клетки все её большие соседи уже посчитаны —
    это топологический порядок DAG, полученный обычной сортировкой.
    Время O(m * n * log(m * n)), память O(m * n). Не боится длинных путей,
    на которых рекурсивная версия упрётся в лимит глубины.
    """
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    best = [[1] * cols for _ in range(rows)]
    cells = sorted(
        ((r, c) for r in range(rows) for c in range(cols)),
        key=lambda cell: matrix[cell[0]][cell[1]],
        reverse=True,
    )
    for r, c in cells:
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best[r][c] = max(best[r][c], 1 + best[nr][nc])
    return max(max(row) for row in best)

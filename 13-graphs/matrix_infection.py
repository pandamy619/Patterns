"""За сколько секунд заражение охватит все здоровые клетки матрицы.

Клетки: 0 — пусто, 1 — здоровая, 2 — заражённая. Каждую секунду заражённая
клетка заражает здоровых соседей по четырём сторонам.
Приём: multi-source BFS (обход в ширину из нескольких источников сразу).
Аналог: LeetCode 994.
"""

from collections import deque

EMPTY, HEALTHY, INFECTED = 0, 1, 2
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def matrix_infection(matrix: list[list[int]]) -> int:
    """Число секунд до полного заражения либо -1, если кто-то недостижим.

    Исходную матрицу не изменяет. Время O(m * n), память O(m * n).
    """
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    grid = [row[:] for row in matrix]

    # В очередь сразу кладём ВСЕ очаги: они стартуют одновременно,
    # как если бы их соединяла с общим «нулевым» источником одна секунда.
    frontier: deque[tuple[int, int]] = deque()
    healthy = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == INFECTED:
                frontier.append((r, c))
            elif grid[r][c] == HEALTHY:
                healthy += 1

    seconds = 0
    # Условие healthy > 0 не даёт засчитать лишнюю секунду за последний слой,
    # которому заражать уже некого.
    while frontier and healthy > 0:
        seconds += 1
        # Обрабатываем ровно один слой: всех, кто был заражён к началу секунды.
        for _ in range(len(frontier)):
            r, c = frontier.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == HEALTHY:
                    grid[nr][nc] = INFECTED      # метка «посещено» и есть заражение
                    healthy -= 1
                    frontier.append((nr, nc))

    return seconds if healthy == 0 else -1

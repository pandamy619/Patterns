"""Наибольшее число точек, лежащих на одной прямой.

Приём: exact slope (точный наклон) — наклон хранится не как float,
а как несократимая пара (dy, dx) с нормализованным знаком; такие пары
служат ключами хеш-таблицы.
Аналог: LeetCode 149.
"""

from collections import defaultdict
from collections.abc import Sequence
from math import gcd


def _slope_key(dy: int, dx: int) -> tuple[int, int]:
    """Канонический вид направления (dy, dx); dy и dx не равны нулю сразу.

    Вертикаль превращается в (1, 0), горизонталь — в (0, 1).
    """
    # gcd неотрицателен и gcd(0, a) == |a|, поэтому отдельная ветка
    # для вертикальных и горизонтальных прямых не нужна — и делить
    # на ноль нигде не приходится.
    divisor = gcd(dy, dx)
    dy //= divisor
    dx //= divisor
    # (1, 2) и (-1, -2) — одна и та же прямая. Договариваемся, что dx > 0,
    # а у вертикали dy > 0.
    if dx < 0 or (dx == 0 and dy < 0):
        dy, dx = -dy, -dx
    return dy, dx


def maximum_collinear_points(points: Sequence[Sequence[int]]) -> int:
    """Максимум точек на одной прямой. Все точки различны.

    Время O(n²) (gcd добавляет логарифм от величины координат),
    память O(n).
    """
    if len(points) <= 2:
        return len(points)

    best = 2
    for i, (x0, y0) in enumerate(points):
        # Все прямые здесь проходят через опорную точку, поэтому одного
        # наклона достаточно, чтобы задать прямую, — свободный член не нужен.
        slope_counts: defaultdict[tuple[int, int], int] = defaultdict(int)

        # Точки левее i можно не смотреть: прямую с лучшим ответом целиком
        # увидит её точка с наименьшим индексом.
        for x1, y1 in points[i + 1:]:
            slope_counts[_slope_key(y1 - y0, x1 - x0)] += 1

        if slope_counts:
            best = max(best, max(slope_counts.values()) + 1)   # +1 — сама опорная
    return best

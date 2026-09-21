"""Сколькими способами можно подняться по лестнице, шагая на 1 или 2 ступени.

Приём: 1D DP (линейная динамика). В файле — весь путь, который стоит пройти
при решении: наивная рекурсия → мемоизация → таблица → две переменные.
Аналог: LeetCode 70.
"""

from functools import lru_cache


def _check(steps: int) -> None:
    if steps < 0:
        raise ValueError("число ступеней не может быть отрицательным")


def climbing_stairs_recursive(steps: int) -> int:
    """Шаг 0: рекурсия «в лоб», только чтобы увидеть формулу.

    Время O(φ^n) — одно и то же поддерево считается снова и снова,
    память O(n) на стек.
    """
    _check(steps)
    # На ступень 0 и на ступень 1 ведёт ровно один маршрут:
    # «стоять на месте» и «один шаг».
    if steps <= 1:
        return 1
    # Последний шаг был либо коротким (с n-1), либо длинным (с n-2).
    # Варианты не пересекаются, поэтому количества складываются.
    return climbing_stairs_recursive(steps - 1) + climbing_stairs_recursive(steps - 2)


def climbing_stairs_memo(steps: int) -> int:
    """Шаг 1: top-down — та же рекурсия, но каждый ответ считается один раз.

    Время O(n), память O(n) (кэш + стек вызовов).
    """
    _check(steps)

    @lru_cache(maxsize=None)
    def ways(step: int) -> int:
        if step <= 1:
            return 1
        return ways(step - 1) + ways(step - 2)

    return ways(steps)


def climbing_stairs_table(steps: int) -> int:
    """Шаг 2: bottom-up — заполняем таблицу от базы к ответу, без рекурсии.

    Время O(n), память O(n).
    """
    _check(steps)
    ways = [1] * (steps + 1)
    # Порядок слева направо: к моменту расчёта ways[i] оба «родителя» готовы.
    for step in range(2, steps + 1):
        ways[step] = ways[step - 1] + ways[step - 2]
    return ways[steps]


def climbing_stairs(steps: int) -> int:
    """Шаг 3: переход смотрит только на два предыдущих значения — их и храним.

    Время O(n), память O(1).
    """
    _check(steps)
    before_last, last = 1, 1          # ways[0], ways[1]
    for _ in range(2, steps + 1):
        before_last, last = last, before_last + last
    return last

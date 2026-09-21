"""Случайный выбор индекса с вероятностью, пропорциональной весу.

Приём: префиксные суммы + lower bound (нижняя граница).
Аналог: LeetCode 528.
"""

import random
from typing import Protocol


class RandomSource(Protocol):
    """Всё, что нам нужно от генератора: целое из отрезка [a, b]."""

    def randint(self, a: int, b: int) -> int: ...


class WeightedRandomSelection:
    """Выбирает индекс i с вероятностью weights[i] / sum(weights).

    Подготовка: O(n) времени и памяти. Каждый вызов pick(): O(log n) времени.
    """

    def __init__(self, weights: list[int], rng: RandomSource | None = None) -> None:
        if any(weight < 0 for weight in weights):
            raise ValueError("веса не могут быть отрицательными")
        if sum(weights) == 0:
            raise ValueError("нужен хотя бы один положительный вес")

        # Представим отрезок длиной total, разрезанный на куски длиной weights[i].
        # prefix[i] — правый конец i-го куска. Массив неубывающий, потому что
        # веса неотрицательны, — а значит, по нему можно искать бинарно.
        self._prefix: list[int] = []
        running = 0
        for weight in weights:
            running += weight
            self._prefix.append(running)

        # Источник случайности передаётся снаружи, чтобы в тестах его можно
        # было подменить и получить детерминированное поведение.
        self._rng: RandomSource = rng if rng is not None else random.Random()

    def pick(self) -> int:
        """Случайный индекс; время O(log n), память O(1)."""
        # Бросаем «дротик» в одну из total единичных клеток: 1..total.
        dart = self._rng.randint(1, self._prefix[-1])

        # Клетка dart принадлежит первому куску, чей правый конец >= dart.
        # hi = n - 1, а не n: dart <= total, поэтому ответ всегда существует.
        lo, hi = 0, len(self._prefix) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self._prefix[mid] >= dart:
                hi = mid
            else:
                lo = mid + 1
        return lo

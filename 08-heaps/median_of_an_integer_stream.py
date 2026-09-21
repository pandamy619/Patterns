"""Медиана потока целых чисел.

Структура данных с двумя операциями: добавить число и узнать медиану
всего, что пришло к этому моменту.

Приём: two heaps. Меньшая половина чисел живёт в max-куче, большая —
в min-куче; медиана всегда на вершинах.
Аналог: LeetCode 295.
"""

from __future__ import annotations

import heapq


class MedianOfAnIntegerStream:
    """Память O(n) на все принятые числа."""

    def __init__(self) -> None:
        # Меньшая половина. Это max-куча, поэтому числа лежат с минусом.
        self._lower: list[int] = []
        # Большая половина, обычная min-куча.
        self._upper: list[int] = []

    def __len__(self) -> int:
        return len(self._lower) + len(self._upper)

    def add(self, num: int) -> None:
        """Принять число. Время O(log n)."""
        # Шаг 1 — порядок: всё, что в lower, не больше всего, что в upper.
        # Число идёт в ту половину, которой принадлежит по значению.
        if not self._lower or num <= -self._lower[0]:
            heapq.heappush(self._lower, -num)
        else:
            heapq.heappush(self._upper, num)

        # Шаг 2 — размеры: половины равны либо lower больше ровно на один.
        # Нарушение возможно только на единицу, так что хватает одной
        # переброски вершины. Переброска порядок не ломает: вершина lower —
        # максимум своей половины, она не больше любого числа из upper.
        if len(self._lower) > len(self._upper) + 1:
            heapq.heappush(self._upper, -heapq.heappop(self._lower))
        elif len(self._upper) > len(self._lower):
            heapq.heappush(self._lower, -heapq.heappop(self._upper))

    def get_median(self) -> float:
        """Медиана принятых чисел. Время O(1)."""
        if not self._lower:
            raise ValueError("медиана пустого потока не определена")
        # Нечётное количество: лишний элемент по договорённости лежит в lower.
        if len(self._lower) > len(self._upper):
            return float(-self._lower[0])
        return (-self._lower[0] + self._upper[0]) / 2

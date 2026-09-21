"""K самых частых строк.

Вернуть k строк с наибольшей частотой, по убыванию частоты; при равной
частоте раньше идёт лексикографически меньшая строка.

Приём: top-k. Два варианта:
  * max-куча из всех уникальных строк (heapify + k извлечений);
  * min-куча размера k — в ней живут только текущие кандидаты в ответ.
Аналог: LeetCode 692.
"""

from __future__ import annotations

import heapq
from collections import Counter


def k_most_frequent_strings_max_heap(strs: list[str], k: int) -> list[str]:
    """Вариант с max-кучей.

    Время O(n + k log u), память O(u), где n — длина входа,
    u — число уникальных строк.
    """
    if k <= 0:
        return []
    freqs = Counter(strs)

    # heapq умеет только min-кучу, поэтому частоту кладём со знаком минус:
    # самая частая строка получает самый маленький ключ и всплывает наверх.
    # Саму строку НЕ «переворачиваем»: при равных частотах кортежи сравнятся
    # по второму полю, и меньшая по алфавиту строка выйдет раньше — ровно то,
    # что требует условие.
    heap = [(-count, word) for word, count in freqs.items()]
    heapq.heapify(heap)  # O(u), а не O(u log u), как u отдельных вставок

    # Уникальных строк может оказаться меньше k — отдаём сколько есть.
    return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]


class _Candidate:
    """Пара (строка, частота) с порядком «хуже — значит меньше».

    В min-куче размера k наверху должен лежать ХУДШИЙ из кандидатов —
    его мы выбрасываем первым. Хуже — это реже, а при равной частоте —
    дальше по алфавиту. Знак числа перевернуть легко, а вот «минус строки»
    не бывает, поэтому обратный порядок строк задаём через __lt__.
    """

    __slots__ = ("word", "count")

    def __init__(self, word: str, count: int) -> None:
        self.word = word
        self.count = count

    def __lt__(self, other: _Candidate) -> bool:
        if self.count != other.count:
            return self.count < other.count
        return self.word > other.word


def k_most_frequent_strings_min_heap(strs: list[str], k: int) -> list[str]:
    """Вариант с min-кучей размера k.

    Время O(n + u log k), память O(u) на счётчик и O(k) на кучу.
    """
    if k <= 0:
        return []
    freqs = Counter(strs)

    heap: list[_Candidate] = []
    for word, count in freqs.items():
        heapq.heappush(heap, _Candidate(word, count))
        # Куча переросла k — худший кандидат (он на вершине) в ответ
        # уже не попадёт: есть k строк лучше него.
        if len(heap) > k:
            heapq.heappop(heap)

    # Куча отдаёт кандидатов от худшего к лучшему, а нужен обратный порядок.
    result = [heapq.heappop(heap).word for _ in range(len(heap))]
    result.reverse()
    return result

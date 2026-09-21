"""Кратчайшая цепочка слов от start до end, где соседние слова отличаются одной буквой.

Все слова цепочки (включая start и end) должны быть в словаре. Ответ — число
СЛОВ в цепочке, 0 — если цепочки нет.
Приём: BFS (обход в ширину) по неявному графу слов; второй вариант —
bidirectional BFS (двунаправленный обход).
Аналог: LeetCode 127 (там start не обязан быть в словаре).
"""

from collections import deque
from collections.abc import Iterator

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _one_letter_variants(word: str) -> Iterator[str]:
    """Все строки, отличающиеся от word ровно одной буквой (их 25 * L).

    Перебираем не пары слов (это O(n) сравнений на каждое слово), а варианты
    замены буквы; есть ли вариант в словаре, вызывающий проверит за O(1).
    """
    for position in range(len(word)):
        prefix, suffix = word[:position], word[position + 1:]
        for letter in ALPHABET:
            if letter != word[position]:
                yield prefix + letter + suffix


def shortest_transformation_sequence(start: str, end: str, dictionary: list[str]) -> int:
    """Обычный BFS от start.

    Время O(n * L^2 * 26): у каждого из n слов 25 * L вариантов, сборка
    и хеширование варианта — O(L). Память O(n * L).
    """
    words = set(dictionary)
    if start not in words or end not in words:
        return 0
    if start == end:
        return 1

    # Слово удаляется из words в момент постановки в очередь — это и есть
    # отметка «посещено». BFS гарантирует, что первое посещение — кратчайшее.
    words.discard(start)
    pending = deque([start])
    length = 1                          # цепочка из одного слова start
    while pending:
        length += 1
        for _ in range(len(pending)):
            word = pending.popleft()
            for neighbor in _one_letter_variants(word):
                if neighbor not in words:
                    continue
                if neighbor == end:
                    return length
                words.discard(neighbor)
                pending.append(neighbor)
    return 0


def shortest_transformation_sequence_bidirectional(
    start: str, end: str, dictionary: list[str]
) -> int:
    """Двунаправленный BFS: два фронта идут навстречу — от start и от end.

    Асимптотика в худшем случае та же, но на практике посещается заметно
    меньше слов: два «шара» радиуса d/2 меньше одного шара радиуса d.
    """
    words = set(dictionary)
    if start not in words or end not in words:
        return 0
    if start == end:
        return 1

    words -= {start, end}               # здесь лежат только НЕпосещённые слова
    front, back = {start}, {end}
    length = 1
    while front and back:
        # Всегда расширяем меньший фронт: так суммарная работа минимальна.
        # Менять фронты местами можно, потому что рёбра неориентированные.
        if len(front) > len(back):
            front, back = back, front
        length += 1
        next_front: set[str] = set()
        for word in front:
            for neighbor in _one_letter_variants(word):
                # Слова встречного фронта уже убраны из words,
                # поэтому встречу проверяем отдельно и в первую очередь.
                if neighbor in back:
                    return length
                if neighbor in words:
                    next_front.add(neighbor)
        words -= next_front
        front = next_front
    return 0

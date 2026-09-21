"""LRU-кэш: get и put за O(1).

Приём: hash map + doubly linked list (хеш-таблица + двусвязный список).
Таблица отвечает за поиск по ключу, список — за порядок «давно → недавно».
Аналог: LeetCode 146.

Модуль намеренно не называется lru_cache.py, чтобы не путаться
с functools.lru_cache.
"""

from __future__ import annotations


class _Entry:
    """Узел двусвязного списка. Ключ хранится тоже: при вытеснении
    по узлу нужно найти и удалить запись в хеш-таблице."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev: _Entry | None = None
        self.next: _Entry | None = None


class LRUCache:
    """Кэш фиксированной ёмкости, вытесняющий самый давно не использованный ключ.

    get и put — O(1) в среднем, память O(capacity).
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("ёмкость кэша должна быть положительной")
        self._capacity = capacity
        self._entries: dict[int, _Entry] = {}

        # Два фиктивных узла по краям: у любого настоящего узла всегда есть
        # оба соседа, и в _unlink/_push_back не нужно ни одной проверки на None.
        self._oldest_side = _Entry(0, 0)   # сразу за ним — кандидат на вытеснение
        self._newest_side = _Entry(0, 0)   # прямо перед ним — самый свежий
        self._oldest_side.next = self._newest_side
        self._newest_side.prev = self._oldest_side

    def get(self, key: int) -> int:
        """Значение по ключу или -1. Обращение делает ключ самым свежим."""
        entry = self._entries.get(key)
        if entry is None:
            return -1
        self._unlink(entry)
        self._push_back(entry)
        return entry.value

    def put(self, key: int, value: int) -> None:
        """Записать пару. Обновление существующего ключа тоже считается использованием."""
        entry = self._entries.get(key)
        if entry is not None:
            entry.value = value
            self._unlink(entry)
            self._push_back(entry)
            return

        if len(self._entries) == self._capacity:
            victim = self._oldest_side.next
            self._unlink(victim)
            # Забыть эту строку — таблица будет расти без ограничений
            # и возвращать значения «вытесненных» ключей.
            del self._entries[victim.key]

        entry = _Entry(key, value)
        self._entries[key] = entry
        self._push_back(entry)

    def __len__(self) -> int:
        return len(self._entries)

    def items(self) -> list[tuple[int, int]]:
        """Пары от самой давней к самой свежей. Нужно для тестов и отладки, O(n)."""
        pairs: list[tuple[int, int]] = []
        entry = self._oldest_side.next
        while entry is not self._newest_side:
            pairs.append((entry.key, entry.value))
            entry = entry.next
        return pairs

    # ----- операции над списком, обе O(1) -----

    def _unlink(self, entry: _Entry) -> None:
        # Именно ради этого список двусвязный: в односвязном за prev
        # пришлось бы идти от головы, и get стал бы O(n).
        entry.prev.next = entry.next
        entry.next.prev = entry.prev

    def _push_back(self, entry: _Entry) -> None:
        last = self._newest_side.prev
        last.next = entry
        entry.prev = last
        entry.next = self._newest_side
        self._newest_side.prev = entry

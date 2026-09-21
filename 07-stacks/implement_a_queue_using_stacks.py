"""Очередь (FIFO), построенная только на двух стеках (LIFO).

Приём: two stacks (два стека) — один принимает элементы, второй отдаёт.
Перекладывание из первого во второй разворачивает порядок, и самый старый
элемент оказывается на вершине.
Аналог: LeetCode 232.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class StackQueue(Generic[T]):
    """Очередь на двух списках, у которых используются только append и pop.

    Любая операция — амортизированно O(1): каждый элемент за всю жизнь
    один раз кладётся в inbox, один раз перекладывается в outbox и один раз
    оттуда вынимается — не больше трёх действий на элемент, сколько бы
    операций ни выполнялось. Отдельный dequeue может стоить O(n), но такой
    дорогой вызов «оплачен» n дешёвыми enqueue перед ним.
    Память O(n).
    """

    def __init__(self) -> None:
        self._inbox: list[T] = []   # сюда приходят новые элементы
        self._outbox: list[T] = []  # отсюда уходят; на вершине — самый старый

    def enqueue(self, item: T) -> None:
        """Добавить элемент в хвост. Время O(1)."""
        self._inbox.append(item)

    def dequeue(self) -> T:
        """Забрать элемент из головы. Амортизированно O(1), в худшем случае O(n)."""
        self._refill()
        return self._outbox.pop()

    def peek(self) -> T:
        """Посмотреть на голову, не забирая. Амортизированно O(1)."""
        self._refill()
        return self._outbox[-1]

    def is_empty(self) -> bool:
        """Время O(1)."""
        return not self._inbox and not self._outbox

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)

    def _refill(self) -> None:
        # Перекладываем, только когда outbox пуст. Иначе свежие элементы
        # легли бы поверх старых и вышли бы раньше них.
        if not self._outbox:
            while self._inbox:
                self._outbox.append(self._inbox.pop())
        if not self._outbox:
            raise IndexError("очередь пуста")

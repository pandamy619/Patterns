"""Сплющить многоуровневый список в одноуровневый.

У узла есть next и child (голова вложенного списка). Основной вариант
выкладывает узлы по уровням: сначала весь верхний уровень, затем все
узлы второго уровня и так далее. Приём: указатель на хвост + второй
указатель, который догоняет его и по дороге дописывает в хвост детей.

Дополнительно — вариант «в глубину», где вложенный список вставляется
сразу после родителя. Близкий аналог именно его — LeetCode 430
(там список двусвязный).
"""

from __future__ import annotations

from linked_lists_helpers import MultiLevelNode


def flatten_multi_level_list(head: MultiLevelNode | None) -> MultiLevelNode | None:
    """Сплющить по уровням, на месте. Все child в результате равны None.

    Время O(n), память O(1).
    """
    if head is None:
        return None

    tail = head
    while tail.next is not None:
        tail = tail.next

    # scan идёт по уже плоской части. Всё, что он дописывает в хвост, он же
    # позже и просмотрит — так очередь обхода в ширину живёт в самом списке.
    scan: MultiLevelNode | None = head
    while scan is not None:
        if scan.child is not None:
            tail.next = scan.child
            # Обнуляем сразу: иначе один узел достижим двумя путями,
            # и результат уже не честный одноуровневый список.
            scan.child = None
            # Хвост только убегает вперёд и ни один узел не проходит дважды,
            # поэтому вложенный while не делает алгоритм квадратичным.
            while tail.next is not None:
                tail = tail.next
        scan = scan.next
    return head


def flatten_multi_level_list_depth_first(
    head: MultiLevelNode | None,
) -> MultiLevelNode | None:
    """Сплющить «в глубину»: вложенный список встаёт сразу за родителем.

    Время O(n), память O(1).
    """
    node = head
    while node is not None:
        if node.child is not None:
            # Ищем хвост только у дочернего ряда. Его собственных детей
            # не трогаем: до них node дойдёт сам и вклеит тем же способом.
            child_tail = node.child
            while child_tail.next is not None:
                child_tail = child_tail.next

            child_tail.next = node.next
            node.next = node.child
            node.child = None
        node = node.next
    return head

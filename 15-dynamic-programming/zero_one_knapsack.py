"""Рюкзак 0/1: каждый предмет можно взять не больше одного раза.

Приём: «взять / не взять». Состояние — (сколько предметов рассмотрено,
какая вместимость доступна); таблица сжимается до одномерного массива.
Аналог: классическая задача 0/1 Knapsack (GeeksforGeeks, AtCoder DP Contest D).
"""


def _check(capacity: int, weights: list[int], values: list[int]) -> None:
    if len(weights) != len(values):
        raise ValueError("у каждого предмета должны быть и вес, и ценность")
    if capacity < 0 or any(weight < 0 for weight in weights):
        raise ValueError("вместимость и веса не могут быть отрицательными")


def _knapsack_table(capacity: int, weights: list[int], values: list[int]) -> list[list[int]]:
    """table[i][c] — лучшая ценность, если доступны первые i предметов и вместимость c."""
    count = len(weights)
    # Строка 0 — «предметов нет», ценность 0 при любой вместимости.
    table = [[0] * (capacity + 1) for _ in range(count + 1)]
    for i in range(1, count + 1):
        weight, value = weights[i - 1], values[i - 1]
        for room in range(capacity + 1):
            table[i][room] = table[i - 1][room]                  # не берём
            if weight <= room:
                # Берём: место под предмет резервируем, остальное заполняем
                # лучшим образом из ПРЕДЫДУЩИХ предметов (строка i - 1).
                table[i][room] = max(table[i][room], table[i - 1][room - weight] + value)
    return table


def zero_one_knapsack_table(capacity: int, weights: list[int], values: list[int]) -> int:
    """Полная таблица.

    Время O(n * capacity), память O(n * capacity).
    """
    _check(capacity, weights, values)
    return _knapsack_table(capacity, weights, values)[-1][-1]


def zero_one_knapsack(capacity: int, weights: list[int], values: list[int]) -> int:
    """Одномерный массив: строка таблицы обновляется на месте.

    Время O(n * capacity), память O(capacity).
    """
    _check(capacity, weights, values)
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        # Обход СПРАВА НАЛЕВО. Клетке room нужно старое значение best[room - weight],
        # то есть клетка левее. Идя справа, мы до неё ещё не добрались, и она хранит
        # данные прошлой строки. Слева направо она была бы уже обновлена — с этим же
        # предметом внутри, — и предмет попал бы в рюкзак дважды.
        for room in range(capacity, weight - 1, -1):
            best[room] = max(best[room], best[room - weight] + value)
    return best[capacity]


def zero_one_knapsack_items(capacity: int, weights: list[int], values: list[int]) -> list[int]:
    """Индексы предметов одного из оптимальных наборов, по возрастанию.

    Время O(n * capacity), память O(n * capacity): для восстановления ответа
    нужна полная таблица.
    """
    _check(capacity, weights, values)
    table = _knapsack_table(capacity, weights, values)
    room = capacity
    chosen: list[int] = []
    for i in range(len(weights), 0, -1):
        # Значение изменилось по сравнению со строкой выше — значит, предмет взяли.
        if table[i][room] != table[i - 1][room]:
            chosen.append(i - 1)
            room -= weights[i - 1]
    return chosen[::-1]

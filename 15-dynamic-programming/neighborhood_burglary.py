"""Максимальная добыча, если нельзя брать два соседних дома.

Приём: 1D DP + выбор «взять / не взять» для каждого дома.
Аналог: LeetCode 198.
"""


def neighborhood_burglary_table(houses: list[int]) -> int:
    """Таблица: best[i] — лучший результат на первых i домах.

    Время O(n), память O(n).
    """
    count = len(houses)
    # Сдвиг на единицу: best[0] — «домов нет». Так база не требует
    # отдельных проверок для одного и двух домов.
    best = [0] * (count + 1)
    for i in range(1, count + 1):
        cash = houses[i - 1]
        skip = best[i - 1]
        # Взяли дом i — значит, дом i-1 трогать нельзя, опираемся на best[i-2].
        take = cash + (best[i - 2] if i >= 2 else 0)
        best[i] = max(skip, take)
    return best[count]


def neighborhood_burglary(houses: list[int]) -> int:
    """То же, но вместо таблицы — два последних значения.

    Время O(n), память O(1).
    """
    two_back, one_back = 0, 0
    for cash in houses:
        two_back, one_back = one_back, max(one_back, two_back + cash)
    return one_back

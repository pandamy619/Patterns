"""Можно ли пройти все курсы, если заданы пары «курс a нужно пройти раньше курса b».

Приём: topological sort (топологическая сортировка) алгоритмом Кана.
Пройти всё можно тогда и только тогда, когда в графе зависимостей нет цикла.
Аналог: LeetCode 207 (там пара записана наоборот: [курс, его пререквизит]).
"""

from collections import deque


def prerequisites(n: int, prerequisite_pairs: list[list[int]]) -> bool:
    """True, если курсы 0..n-1 можно выстроить в допустимом порядке.

    Время O(n + e), память O(n + e), где e — число пар.
    """
    unlocks: list[list[int]] = [[] for _ in range(n)]   # a -> курсы, которые он открывает
    blockers = [0] * n                                  # входящая степень: сколько курсов ещё мешают
    for before, after in prerequisite_pairs:
        unlocks[before].append(after)
        blockers[after] += 1        # повтор пары попадёт и в список, и в счётчик — баланс сохранится

    # Курсы без пререквизитов можно брать сразу.
    available = deque(course for course in range(n) if blockers[course] == 0)
    taken = 0
    while available:
        course = available.popleft()
        taken += 1
        for nxt in unlocks[course]:
            blockers[nxt] -= 1
            if blockers[nxt] == 0:
                available.append(nxt)

    # Курс на цикле никогда не дождётся нуля: ему мешает другой курс цикла,
    # а тому — он сам. Поэтому «взяли не все» означает ровно «есть цикл».
    return taken == n

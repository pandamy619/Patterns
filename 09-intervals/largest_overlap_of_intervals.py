"""Наибольшее число интервалов, активных одновременно.

Приём: sweep line (заметающая прямая).
Интервалы ПОЛУОТКРЫТЫЕ, [start, end): начало входит, конец — нет.
Поэтому [1, 3) и [3, 5) не пересекаются: в точке 3 первый уже закончился.
Аналог: LeetCode 253 (Meeting Rooms II), LintCode 919.
"""

START = 1
END = -1


def largest_overlap_of_intervals(intervals: list[list[int]]) -> int:
    """Вариант с единым списком событий.

    Время O(n log n), память O(n).
    """
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, START))
        events.append((end, END))

    # Кортежи сравниваются поэлементно, а END = -1 < START = 1, так что в одной
    # точке закрытия идут раньше открытий. Для полуоткрытых интервалов это
    # и нужно: сначала освобождаем место, потом занимаем.
    events.sort()

    active = 0
    best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best


def largest_overlap_two_arrays(intervals: list[list[int]]) -> int:
    """Тот же sweep line без списка событий: начала и концы сортируются
    отдельно, а по ним идут два указателя.

    Время O(n log n), память O(n).
    """
    starts = sorted(start for start, _ in intervals)
    ends = sorted(end for _, end in intervals)

    active = 0
    best = 0
    closed = 0
    for start in starts:
        # Закрываем всё, что закончилось к моменту start включительно:
        # конец в полуоткрытом интервале не входит. Какой именно интервал
        # закрылся, неважно — счётчику нужно только количество.
        # Проверка границы срабатывает только на вырожденных интервалах
        # вида [5, 5): при start < end хотя бы один конец всегда правее start.
        while closed < len(ends) and ends[closed] <= start:
            active -= 1
            closed += 1
        active += 1
        best = max(best, active)
    return best

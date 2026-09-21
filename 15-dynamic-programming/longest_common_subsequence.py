"""Длина наибольшей общей подпоследовательности двух строк (LCS).

Приём: DP по двум строкам — состояние задаётся парой префиксов.
Аналог: LeetCode 1143.
"""


def _lcs_table(first: str, second: str) -> list[list[int]]:
    """table[i][j] — LCS префиксов first[:i] и second[:j]."""
    rows, cols = len(first), len(second)
    # Нулевые строка и столбец — пустые префиксы: общего у них ничего нет.
    table = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if first[i - 1] == second[j - 1]:
                # Одинаковые последние символы выгодно спарить друг с другом:
                # любую другую пару для одного из них можно заменить на эту
                # и ничего не потерять.
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                # Хотя бы один из двух последних символов в ответ не входит —
                # пробуем выбросить каждый.
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def longest_common_subsequence(first: str, second: str) -> int:
    """Полная таблица.

    Время O(m * n), память O(m * n).
    """
    return _lcs_table(first, second)[-1][-1]


def longest_common_subsequence_two_rows(first: str, second: str) -> int:
    """Переход смотрит только на предыдущую строку таблицы — храним две строки.

    Время O(m * n), память O(min(m, n)).
    """
    # Строка таблицы идёт вдоль second, поэтому короткую строку ставим на его место.
    if len(second) > len(first):
        first, second = second, first
    previous = [0] * (len(second) + 1)
    for symbol in first:
        current = [0] * (len(second) + 1)
        for j, other in enumerate(second, start=1):
            if symbol == other:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def restore_common_subsequence(first: str, second: str) -> str:
    """Сама подпоследовательность (одна из возможных), а не только длина.

    Время O(m * n), память O(m * n): для восстановления нужна вся таблица,
    сжать её до двух строк здесь уже нельзя.
    """
    table = _lcs_table(first, second)
    i, j = len(first), len(second)
    picked: list[str] = []
    # Идём из правого нижнего угла и повторяем решения, принятые при заполнении.
    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            picked.append(first[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(picked))

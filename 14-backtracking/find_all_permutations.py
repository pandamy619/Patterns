"""Все перестановки массива различных чисел.

Приём: choose → explore → unchoose. На каждом уровне дерева решений выбираем
любой ещё не занятый элемент, уходим глубже, а вернувшись — освобождаем его.
Аналог: LeetCode 46.
"""


def find_all_permutations(nums: list[int]) -> list[list[int]]:
    """Вернуть все перестановки nums (элементы различны).

    Порядок ответа — лексикографический по индексам исходного массива.
    У пустого массива ровно одна перестановка — пустая.

    Время O(n · n!): листьев n!, в каждом копируем путь длины n.
    Память O(n) сверх ответа: путь, отметки и глубина рекурсии.
    """
    result: list[list[int]] = []
    path: list[int] = []
    # Отметки по индексам, а не множество значений: проверка за O(1)
    # и никаких требований к хешируемости элементов.
    taken = [False] * len(nums)

    def extend() -> None:
        if len(path) == len(nums):
            # path живёт один на всю рекурсию и дальше будет меняться,
            # поэтому в ответ кладём копию.
            result.append(path.copy())
            return
        for index, value in enumerate(nums):
            if taken[index]:
                continue
            taken[index] = True          # выбрать
            path.append(value)
            extend()                     # рекурсия
            path.pop()                   # отменить выбор —
            taken[index] = False         # строго в обратном порядке

    extend()
    return result

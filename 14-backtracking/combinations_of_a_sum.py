"""Все комбинации чисел с заданной суммой; каждое число можно брать многократно.

Приём: start index + pruning. Стартовый индекс запрещает возвращаться
к числам левее текущего — так комбинации получаются неубывающими и не
повторяются с точностью до порядка. Сортировка позволяет оборвать цикл,
как только очередное число перестало помещаться в остаток.
Аналог: LeetCode 39.
"""


def combinations_of_a_sum(nums: list[int], target: int) -> list[list[int]]:
    """Вернуть все комбинации чисел из nums с суммой target.

    Числа положительные и различные, каждое можно использовать сколько
    угодно раз. Комбинации, отличающиеся только порядком, считаются одной;
    каждая возвращается в неубывающем порядке. Для target = 0 ответ —
    одна пустая комбинация, для target < 0 — ничего.

    Время O(n^(target / min)) в худшем случае: глубина дерева не больше
    target / min(nums), ветвление не больше n. Память O(target / min)
    сверх ответа.
    """
    if any(value <= 0 for value in nums):
        # С нулём рекурсия не закончилась бы: сумма не растёт, а брать можно вечно.
        raise ValueError("all numbers must be positive")

    candidates = sorted(set(nums))
    result: list[list[int]] = []
    combo: list[int] = []

    def fill(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(combo.copy())
            return
        for index in range(start, len(candidates)):
            value = candidates[index]
            if value > remaining:
                # Кандидаты отсортированы: все следующие ещё больше,
                # поэтому выходим из цикла, а не просто пропускаем.
                break
            combo.append(value)
            # Передаём index, а не index + 1: то же число можно взять ещё раз.
            fill(index, remaining - value)
            combo.pop()

    if target >= 0:
        fill(0, target)
    return result

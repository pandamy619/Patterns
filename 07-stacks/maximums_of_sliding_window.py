"""Максимум в каждом окне длины k.

Приём: monotonic deque (монотонный дек) — тот же монотонный стек, у которого
открыт ещё и второй конец: справа выталкиваем «безнадёжных» кандидатов,
слева — тех, кто выехал за границу окна.
Аналог: LeetCode 239.
"""

from collections import deque


def maximums_of_sliding_window(nums: list[int], k: int) -> list[int]:
    """Вернуть максимумы окон nums[i : i + k] для всех i слева направо.

    Если k больше длины массива, окон нет — ответ пустой.
    Время O(n): каждый индекс один раз входит в дек и не более раза выходит.
    Память O(k).
    """
    if k <= 0:
        raise ValueError("размер окна должен быть положительным")

    maximums: list[int] = []
    candidates: deque[int] = deque()  # индексы; значения убывают слева направо
    for right, value in enumerate(nums):
        # Кандидат, который и старше, и не больше нового числа, максимумом
        # уже не станет: новое число переживёт его в любом будущем окне.
        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(right)
        # Слева стоит самый старый индекс; за границу окна мог выйти только он.
        if candidates[0] <= right - k:
            candidates.popleft()
        if right >= k - 1:
            maximums.append(nums[candidates[0]])
    return maximums

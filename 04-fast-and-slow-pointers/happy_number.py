"""Счастливое число: приводит ли к 1 повторная замена числа суммой квадратов цифр.

Приём: cycle detection на неявном списке. Узел — число, «ссылка next» —
функция перехода, так что хранить пройденные числа незачем.
Аналог: LeetCode 202.
"""


def _digit_square_sum(number: int) -> int:
    """Сумма квадратов десятичных цифр."""
    total = 0
    while number > 0:
        number, digit = divmod(number, 10)
        total += digit * digit
    return total


def happy_number(n: int) -> bool:
    """Вернуть True, если цепочка n -> сумма квадратов цифр -> ... доходит до 1.

    Время O(log n), память O(1): дороже всего первый шаг (у n порядка log n цифр),
    дальше цепочка живёт среди чисел не больше 243, и число шагов там
    ограничено константой.
    """
    if n < 1:
        raise ValueError("ожидается положительное целое число")
    slow = fast = n
    while True:
        slow = _digit_square_sum(slow)
        fast = _digit_square_sum(_digit_square_sum(fast))
        # Единица переходит сама в себя, то есть это тоже цикл, только длины 1.
        # Значит встреча случится в любом случае, и вопрос лишь в том — где.
        if slow == fast:
            return slow == 1

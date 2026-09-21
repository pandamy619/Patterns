"""Вычислить выражение с целыми числами, «+», «-», скобками и пробелами.

Приём: nested context (сохранение контекста) — на открывающей скобке кладём
в стек недосчитанную внешнюю сумму и знак перед скобкой, на закрывающей —
достаём и продолжаем с того же места.
Аналог: LeetCode 224.
"""

_DIGITS = "0123456789"


def evaluate_expression(expression: str) -> int:
    """Вернуть значение корректного выражения. Встроенный eval не используется.

    Поддерживается унарный знак перед числом и перед скобкой: "-(4 - 9)", "3 - -2".
    Время O(n), память O(d), где d — глубина вложенности скобок.
    """
    total = 0        # сумма уже завершённых слагаемых на текущем уровне скобок
    sign = 1         # знак слагаемого, которое сейчас читаем
    number = 0       # само слагаемое: число по цифрам или значение скобки
    saved: list[tuple[int, int]] = []  # (внешняя сумма, знак перед скобкой)
    # True, пока слагаемое ещё не началось: в начале, после оператора, после "(".
    # Знак в такой позиции — унарный, он не завершает никакого слагаемого.
    operand_expected = True

    for symbol in expression:
        if symbol in _DIGITS:
            number = number * 10 + int(symbol)
            operand_expected = False
        elif symbol in "+-":
            if operand_expected:
                if symbol == "-":
                    sign = -sign
            else:
                # Бинарный оператор: предыдущее слагаемое закончилось.
                total += sign * number
                number = 0
                sign = 1 if symbol == "+" else -1
                operand_expected = True
        elif symbol == "(":
            # Внутри скобок — самостоятельное выражение, считаем его с нуля,
            # а всё, что знали про внешний уровень, прячем в стек.
            saved.append((total, sign))
            total, sign = 0, 1
            operand_expected = True
        elif symbol == ")":
            total += sign * number
            outer_total, outer_sign = saved.pop()
            # Для внешнего уровня вся скобка — просто очередное слагаемое.
            number = total
            total, sign = outer_total, outer_sign
            operand_expected = False
        elif not symbol.isspace():
            raise ValueError(f"неожиданный символ: {symbol!r}")

    return total + sign * number

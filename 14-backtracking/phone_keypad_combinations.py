"""Все буквенные сочетания, которые можно набрать данной строкой цифр.

Приём: choose → explore → unchoose. Уровень дерева решений — очередная
цифра, ветки — буквы на её кнопке.
Аналог: LeetCode 17.
"""

KEYPAD: dict[str, str] = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def phone_keypad_combinations(digits: str) -> list[str]:
    """Вернуть все строки, соответствующие цифрам digits (только «2»–«9»).

    Для пустой строки ответ — пустой список: набирать нечего.

    Время O(n · 4^n): листьев не больше 4^n, склейка строки в листе — O(n).
    Память O(n) сверх ответа.
    """
    for digit in digits:
        if digit not in KEYPAD:
            raise ValueError(f"no letters on key {digit!r}")
    if not digits:
        return []

    result: list[str] = []
    letters: list[str] = []  # список, а не строка: append/pop за O(1)

    def press(position: int) -> None:
        if position == len(digits):
            result.append("".join(letters))
            return
        for letter in KEYPAD[digits[position]]:
            letters.append(letter)
            press(position + 1)
            letters.pop()

    press(0)
    return result

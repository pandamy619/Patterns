"""Все подмножества массива различных чисел.

Приём: include / exclude. Про каждый элемент по очереди принимаем одно
из двух решений — «не брать» или «брать»; лист дерева — готовое подмножество.
Аналог: LeetCode 78.
"""


def find_all_subsets(nums: list[int]) -> list[list[int]]:
    """Вернуть все 2^n подмножеств nums (элементы различны).

    Внутри подмножества сохраняется порядок исходного массива.

    Время O(n · 2^n): листьев 2^n, копия пути в листе стоит до n.
    Память O(n) сверх ответа: путь и глубина рекурсии.
    """
    result: list[list[int]] = []
    chosen: list[int] = []

    def decide(position: int) -> None:
        if position == len(nums):
            result.append(chosen.copy())
            return
        # Ветка «не брать»: состояние не менялось, отменять нечего.
        decide(position + 1)
        # Ветка «брать»: классическая тройка выбрать → рекурсия → отменить.
        chosen.append(nums[position])
        decide(position + 1)
        chosen.pop()

    decide(0)
    return result

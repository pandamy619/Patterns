"""Для каждой позиции — произведение всех элементов, кроме неё самой.

Делить нельзя, дополнительной памяти, кроме массива ответа, — O(1).
Идея: ответ для позиции i — это (произведение всего, что левее) на
(произведение всего, что правее). Левые произведения копим прямым проходом
прямо в массиве ответа, правые — обратным проходом в одной переменной.
Аналог: LeetCode 238.
"""


def product_array_without_current_element(nums: list[int]) -> list[int]:
    """Вернуть массив, где result[i] — произведение всех nums, кроме nums[i].

    Время O(n), память O(1), не считая массива ответа.
    """
    size = len(nums)
    result = [1] * size

    # Проход слева направо: в result[i] кладём произведение nums[0..i-1].
    # Сначала записываем, потом домножаем — так nums[i] в свою ячейку не попадёт.
    left = 1
    for i in range(size):
        result[i] = left
        left *= nums[i]

    # Проход справа налево: домножаем на произведение nums[i+1..].
    # Отдельный массив суффиксов не нужен: в каждый момент нужен только
    # один его элемент, он живёт в переменной right.
    right = 1
    for i in range(size - 1, -1, -1):
        result[i] *= right
        right *= nums[i]

    return result


def product_array_with_division(nums: list[int]) -> list[int]:
    """Вариант «а если бы делить было можно» — с аккуратной обработкой нулей.

    Время O(n), память O(1), не считая массива ответа.
    """
    zeros = 0
    product_of_nonzero = 1
    for value in nums:
        if value == 0:
            zeros += 1
        else:
            product_of_nonzero *= value

    # Два нуля и больше: какой элемент ни убери, хотя бы один ноль останется.
    if zeros >= 2:
        return [0] * len(nums)
    # Ровно один ноль: ненулевой ответ только на его собственной позиции.
    if zeros == 1:
        return [product_of_nonzero if value == 0 else 0 for value in nums]
    # Нулей нет: делится всегда нацело, потому что value — один из множителей.
    return [product_of_nonzero // value for value in nums]

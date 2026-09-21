"""Обход матрицы по спирали по часовой стрелке.

Приём: shrinking boundaries (сжимающиеся границы) — четыре индекса
описывают ещё не пройденный прямоугольник, после каждой стороны он сужается.
Аналог: LeetCode 54.
"""


def spiral_traversal(matrix: list[list[int]]) -> list[int]:
    """Элементы матрицы в порядке спирали: вправо, вниз, влево, вверх.

    Время O(m * n), память O(1) сверх ответа.
    """
    if not matrix or not matrix[0]:
        return []

    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    order: list[int] = []

    while top <= bottom and left <= right:
        # Верхняя сторона целиком, включая оба угла.
        for col in range(left, right + 1):
            order.append(matrix[top][col])
        top += 1

        # Правая сторона. Верхний угол уже взят — top сдвинут, повтора не будет.
        for row in range(top, bottom + 1):
            order.append(matrix[row][right])
        right -= 1

        # После двух сдвигов прямоугольник мог схлопнуться. Если осталась
        # одна строка, она уже пройдена слева направо — обратный проход
        # выдал бы её второй раз.
        if top <= bottom:
            for col in range(right, left - 1, -1):
                order.append(matrix[bottom][col])
            bottom -= 1

        # То же самое для единственного столбца.
        if left <= right:
            for row in range(bottom, top - 1, -1):
                order.append(matrix[row][left])
            left += 1

    return order

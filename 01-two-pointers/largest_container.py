"""Наибольший объём воды между двумя вертикальными линиями.

Стратегия: inward traversal (встречное движение) с жадным выбором,
какой указатель двигать.
Аналог: LeetCode 11.
"""


def largest_container(heights: list[int]) -> int:
    """Максимум min(h[i], h[j]) * (j - i) по всем парам i < j.

    Время O(n), память O(1).
    """
    lo, hi = 0, len(heights) - 1
    best = 0
    while lo < hi:
        water = min(heights[lo], heights[hi]) * (hi - lo)
        best = max(best, water)
        # Объём ограничен низкой стенкой. Если сдвинуть высокую, ширина
        # уменьшится, а высота не вырастет — лучше точно не станет.
        # Значит, низкую стенку можно отбросить навсегда.
        if heights[lo] < heights[hi]:
            lo += 1
        else:
            hi -= 1
    return best

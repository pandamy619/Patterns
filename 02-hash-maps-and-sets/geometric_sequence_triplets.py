"""Количество троек, образующих геометрическую прогрессию.

Идея: перебираем СРЕДНИЙ элемент, а сколько подходящих соседей слева
и справа — узнаём из двух частотных хеш-таблиц.
Аналог: HackerRank «Count Triplets».
"""

from collections import Counter


def geometric_sequence_triplets(nums: list[int], ratio: int) -> int:
    """Число троек индексов i < j < k, где nums[j] = nums[i] * ratio
    и nums[k] = nums[j] * ratio. Знаменатель ratio — ненулевое целое.

    Время O(n), память O(n).
    """
    if ratio == 0:
        raise ValueError("ratio must be non-zero")

    left: Counter[int] = Counter()   # частоты элементов левее текущего
    right: Counter[int] = Counter(nums)  # частоты элементов правее текущего
    total = 0

    for middle in nums:
        right[middle] -= 1  # текущий элемент больше не «справа»
        if middle % ratio == 0:
            # Каждая пара (левый, правый) даёт отдельную тройку — перемножаем.
            total += left[middle // ratio] * right[middle * ratio]
        left[middle] += 1
    return total

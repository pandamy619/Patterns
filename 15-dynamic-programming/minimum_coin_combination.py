"""Минимальное число монет, которыми можно набрать сумму (монет каждого вида — сколько угодно).

Приём: 1D DP по сумме; внутри — перебор «какой монетой закончили».
Это «рюкзак без ограничения на количество» (unbounded knapsack).
Аналог: LeetCode 322.
"""

from functools import lru_cache

# «Сумму набрать нельзя». Бесконечность удобнее, чем -1: с ней min() работает
# без особых случаев, а inf + 1 по-прежнему inf.
UNREACHABLE = float("inf")


def _check(coins: list[int], target: int) -> None:
    if target < 0:
        raise ValueError("сумма не может быть отрицательной")
    if any(coin <= 0 for coin in coins):
        raise ValueError("номиналы должны быть положительными")


def minimum_coin_combination(coins: list[int], target: int) -> int:
    """Bottom-up: fewest[a] — минимум монет для суммы a.

    Время O(target * len(coins)), память O(target).
    """
    _check(coins, target)
    fewest: list[float] = [0] + [UNREACHABLE] * target
    for amount in range(1, target + 1):
        for coin in coins:
            # Последней положили монету coin — значит, до неё была набрана
            # сумма amount - coin, и набрана оптимально.
            if coin <= amount and fewest[amount - coin] + 1 < fewest[amount]:
                fewest[amount] = fewest[amount - coin] + 1
    return -1 if fewest[target] == UNREACHABLE else int(fewest[target])


def minimum_coin_combination_memo(coins: list[int], target: int) -> int:
    """Top-down: та же формула, но считаются только достижимые остатки.

    Время O(target * len(coins)), память O(target). Глубина рекурсии доходит
    до target / min(coins) — для больших сумм в Python нужен bottom-up.
    """
    _check(coins, target)

    @lru_cache(maxsize=None)
    def fewest(amount: int) -> float:
        if amount == 0:
            return 0
        best = UNREACHABLE
        for coin in coins:
            if coin <= amount:
                best = min(best, fewest(amount - coin) + 1)
        return best

    answer = fewest(target)
    return -1 if answer == UNREACHABLE else int(answer)

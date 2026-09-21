"""Тесты к паттерну Greedy.

Жадный алгоритм легко написать и легко написать неправильно, поэтому каждое
решение сверяется с эталоном, в котором жадности нет вовсе: полный перебор
или честная симуляция. Эталоны медленные, зато очевидно правильные.
"""

import random
from functools import lru_cache
from itertools import product

import pytest

from candies import candies, distribute_candies
from gas_stations import gas_stations
from jump_to_the_end import jump_to_the_end, jump_to_the_end_backward

RNG = random.Random(2024)
ROUNDS = 400


# ---------- jump_to_the_end ----------

def _jump_brute(nums):
    """Обход всех прыжков подряд: никаких догадок про «самый дальний»."""
    visited = {0}
    stack = [0]
    while stack:
        index = stack.pop()
        for step in range(1, nums[index] + 1):
            target = index + step
            if target < len(nums) and target not in visited:
                visited.add(target)
                stack.append(target)
    return len(nums) - 1 in visited


@pytest.mark.parametrize("solve", [jump_to_the_end, jump_to_the_end_backward])
def test_jump_to_the_end_examples(solve):
    assert solve([2, 3, 0, 0, 1, 0]) is True
    assert solve([1, 2, 0, 0, 4]) is False          # упираемся в нули
    assert solve([0]) is True                       # уже на финише
    assert solve([0, 1]) is False                   # с места не сдвинуться
    assert solve([5, 0, 0, 0, 0, 0]) is True        # один прыжок через нули
    assert solve([4, 0, 0, 0, 0, 0]) is False       # не хватило одного шага
    assert solve([1, 1, 1, 1]) is True
    assert solve([3, 2, 1, 0, 0]) is False          # все дороги ведут в ноль
    assert solve([100]) is True


@pytest.mark.parametrize("solve", [jump_to_the_end, jump_to_the_end_backward])
def test_jump_to_the_end_random(solve):
    for _ in range(ROUNDS):
        # Много нулей и короткие прыжки — чтобы ответы False встречались часто.
        nums = [RNG.choice([0, 0, 1, 1, 2, 3]) for _ in range(RNG.randint(1, 12))]
        assert solve(nums) == _jump_brute(nums), nums


# ---------- gas_stations ----------

def _can_complete_from(gas, cost, start):
    tank = 0
    n = len(gas)
    for shift in range(n):
        station = (start + shift) % n
        tank += gas[station] - cost[station]
        if tank < 0:
            return False
    return True


def _gas_brute(gas, cost):
    """Честно пробуем стартовать с каждой станции."""
    for start in range(len(gas)):
        if _can_complete_from(gas, cost, start):
            return start
    return -1


def test_gas_stations_examples():
    assert gas_stations([1, 4, 2, 6, 3], [3, 5, 1, 2, 5]) == 2   # бак доходит до нуля
    assert gas_stations([2, 2, 2], [3, 3, 3]) == -1              # топлива мало в сумме
    assert gas_stations([5], [4]) == 0
    assert gas_stations([4], [5]) == -1
    assert gas_stations([0], [0]) == 0
    assert gas_stations([0, 0, 9], [3, 3, 3]) == 2               # старт с последней станции
    assert gas_stations([3, 1, 1], [1, 2, 2]) == 0               # старт с первой
    assert gas_stations([1, 1, 1], [1, 1, 1]) == 0               # подходят все — берём меньший
    assert gas_stations([], []) == -1


def test_gas_stations_rejects_different_lengths():
    with pytest.raises(ValueError):
        gas_stations([1, 2], [1])


def test_gas_stations_random():
    for _ in range(ROUNDS):
        n = RNG.randint(1, 9)
        gas = [RNG.randint(0, 6) for _ in range(n)]
        cost = [RNG.randint(0, 6) for _ in range(n)]
        assert gas_stations(gas, cost) == _gas_brute(gas, cost), (gas, cost)


def test_gas_stations_random_balanced():
    # Суммы равны — самый коварный случай: круг проходится «впритык».
    for _ in range(ROUNDS):
        n = RNG.randint(1, 9)
        gas = [RNG.randint(0, 6) for _ in range(n)]
        cost = gas[:]
        RNG.shuffle(cost)
        answer = gas_stations(gas, cost)
        assert answer == _gas_brute(gas, cost), (gas, cost)
        assert answer != -1


# ---------- candies ----------

def _is_fair(ratings, portions):
    if any(p < 1 for p in portions):
        return False
    for i in range(len(ratings) - 1):
        if ratings[i] > ratings[i + 1] and not portions[i] > portions[i + 1]:
            return False
        if ratings[i] < ratings[i + 1] and not portions[i] < portions[i + 1]:
            return False
    return True


def _candies_brute(ratings):
    """Перебор всех раздач. Больше n конфет одному ребёнку не нужно никогда."""
    n = len(ratings)
    return min(
        sum(portions)
        for portions in product(range(1, n + 1), repeat=n)
        if _is_fair(ratings, portions)
    ) if n else 0


def _candies_by_relaxation(ratings):
    """Эталон для длинных массивов: начинаем с единиц и поднимаем порцию
    только там, где правило нарушено, и только на необходимый минимум."""
    portions = [1] * len(ratings)
    changed = True
    while changed:
        changed = False
        for i in range(len(ratings)):
            for j in (i - 1, i + 1):
                if 0 <= j < len(ratings) and ratings[i] > ratings[j] and portions[i] <= portions[j]:
                    portions[i] = portions[j] + 1
                    changed = True
    return portions


def test_candies_examples():
    assert distribute_candies([5, 2, 4, 7, 7, 3, 1]) == [2, 1, 2, 3, 3, 2, 1]
    assert candies([5, 2, 4, 7, 7, 3, 1]) == 14
    assert candies([]) == 0
    assert candies([9]) == 1
    assert candies([3, 3, 3, 3]) == 4               # равным соседям лишнего не надо
    assert candies([1, 2, 3, 4]) == 10              # лесенка вверх
    assert candies([4, 3, 2, 1]) == 10              # лесенка вниз
    assert candies([1, 5, 1]) == 4
    assert candies([5, 1, 5]) == 5
    assert candies([1, 2, 9, 3, 2, 1]) == 13        # пик: max(3, 4) = 4
    assert candies([1, 2, 3, 9, 2]) == 11           # пик: max(4, 2) = 4, без max сломается
    assert candies([2, 2, 1]) == 4                  # равный сосед может получить меньше


def test_candies_random_against_full_enumeration():
    for _ in range(ROUNDS):
        ratings = [RNG.randint(1, 4) for _ in range(RNG.randint(0, 5))]
        assert candies(ratings) == _candies_brute(ratings), ratings
        assert _is_fair(ratings, distribute_candies(ratings))


def test_candies_random_against_relaxation():
    for _ in range(ROUNDS):
        ratings = [RNG.randint(1, 6) for _ in range(RNG.randint(0, 40))]
        assert distribute_candies(ratings) == _candies_by_relaxation(ratings), ratings


# ---------- контрпример из README: где жадность ломается ----------

def _coins_greedy(coins, amount):
    """«Бери самую крупную монету, какая влезает» — без права передумать."""
    used = 0
    for coin in sorted(coins, reverse=True):
        used += amount // coin
        amount %= coin
    return used if amount == 0 else -1


def _coins_exact(coins, amount):
    @lru_cache(maxsize=None)
    def best(rest):
        if rest == 0:
            return 0
        options = [best(rest - coin) for coin in coins if coin <= rest]
        options = [value for value in options if value != -1]
        return 1 + min(options) if options else -1

    return best(amount)


def test_greedy_coin_change_counterexample():
    # Числа из README: набор {1, 4, 6}, сумма 8.
    assert _coins_greedy((1, 4, 6), 8) == 3         # 6 + 1 + 1
    assert _coins_exact((1, 4, 6), 8) == 2          # 4 + 4
    # А на «хорошем» наборе та же жадность не ошибается ни разу.
    for amount in range(0, 200):
        assert _coins_greedy((1, 5, 10, 25), amount) == _coins_exact((1, 5, 10, 25), amount)

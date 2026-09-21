"""Тесты к паттерну Stacks.

Кроме ручных примеров каждое решение сверяется с медленным, но очевидно
правильным эталоном на случайных данных. Для очереди эталон —
collections.deque, для выражений — значение, посчитанное при генерации
(и дополнительно eval: выражения собираются из безопасного набора символов).
"""

import random
from collections import deque

import pytest

from evaluate_expression import evaluate_expression
from implement_a_queue_using_stacks import StackQueue
from maximums_of_sliding_window import maximums_of_sliding_window
from next_largest_number_to_the_right import next_largest_number_to_the_right
from repeated_removal_of_adjacent_duplicates import repeated_removal_of_adjacent_duplicates
from valid_parenthesis_expression import valid_parenthesis_expression

RNG = random.Random(2024)
ROUNDS = 500


# ---------- valid_parenthesis_expression ----------

def _parenthesis_brute(text):
    # Корректная последовательность всегда содержит «голую» пару вида "()".
    # Вычёркиваем такие пары, пока получается; от корректной не останется ничего.
    previous = None
    while previous != text:
        previous = text
        for pair in ("()", "[]", "{}"):
            text = text.replace(pair, "")
    return text == ""


def test_valid_parenthesis_expression_examples():
    assert valid_parenthesis_expression("{[()]}()")
    assert valid_parenthesis_expression("")
    assert not valid_parenthesis_expression("[(])")      # пары есть, порядок не тот
    assert not valid_parenthesis_expression("(((")       # остались незакрытые
    assert not valid_parenthesis_expression(")")         # закрывать нечего
    assert not valid_parenthesis_expression("())(")      # поровну, но неверно
    assert not valid_parenthesis_expression("(}")
    assert valid_parenthesis_expression("f(a[0]) { }")   # прочие символы не мешают


def test_valid_parenthesis_expression_random():
    seen_valid = 0
    for _ in range(ROUNDS):
        text = "".join(RNG.choice("()[]{}") for _ in range(RNG.randint(0, 8)))
        expected = _parenthesis_brute(text)
        seen_valid += expected
        assert valid_parenthesis_expression(text) == expected
    assert seen_valid > 10  # иначе тест проверял бы только ответ False


def _random_valid_brackets(depth):
    if depth == 0 or RNG.random() < 0.25:
        return ""
    opener, closer = RNG.choice(["()", "[]", "{}"])
    return opener + _random_valid_brackets(depth - 1) + closer + _random_valid_brackets(depth - 1)


def test_valid_parenthesis_expression_random_valid_and_broken():
    for _ in range(ROUNDS):
        text = _random_valid_brackets(4)
        assert valid_parenthesis_expression(text)
        if text:
            # Удаление любого одного символа делает длину нечётной.
            cut = RNG.randrange(len(text))
            assert not valid_parenthesis_expression(text[:cut] + text[cut + 1:])


# ---------- next_largest_number_to_the_right ----------

def _next_largest_brute(nums):
    return [
        next((later for later in nums[i + 1:] if later > value), -1)
        for i, value in enumerate(nums)
    ]


def test_next_largest_number_to_the_right_examples():
    assert next_largest_number_to_the_right([3, 8, 4, 1, 7, 9]) == [8, 9, 7, 7, 9, -1]
    assert next_largest_number_to_the_right([1, 2, 3]) == [2, 3, -1]
    assert next_largest_number_to_the_right([3, 2, 1]) == [-1, -1, -1]
    assert next_largest_number_to_the_right([5, 5, 5]) == [-1, -1, -1]   # равное — не большее
    assert next_largest_number_to_the_right([-4, -9, -2]) == [-2, -2, -1]
    assert next_largest_number_to_the_right([7]) == [-1]
    assert next_largest_number_to_the_right([]) == []


def test_next_largest_number_to_the_right_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(0, 9) for _ in range(RNG.randint(0, 10))]
        assert next_largest_number_to_the_right(nums) == _next_largest_brute(nums)


def test_next_largest_number_to_the_right_is_linear():
    # На убывающем массиве стек вырастает до n, на возрастающем — не растёт вовсе.
    size = 200_000
    assert next_largest_number_to_the_right(list(range(size, 0, -1))) == [-1] * size
    assert next_largest_number_to_the_right(list(range(size)))[:-1] == list(range(1, size))


# ---------- evaluate_expression ----------

def _spaces():
    return " " * RNG.choice([0, 0, 1, 2])


def _random_expression(depth):
    """Вернуть (текст, значение): значение считается по дереву, без разбора текста."""
    text, value = _random_operand(depth)
    for _ in range(RNG.randint(0, 3)):
        operator = RNG.choice("+-")
        operand_text, operand_value = _random_operand(depth)
        text += _spaces() + operator + _spaces() + operand_text
        value = value + operand_value if operator == "+" else value - operand_value
    return text, value


def _random_operand(depth):
    if depth > 0 and RNG.random() < 0.4:
        inner_text, value = _random_expression(depth - 1)
        text = "(" + _spaces() + inner_text + _spaces() + ")"
    else:
        value = RNG.choice([0, RNG.randint(0, 9), RNG.randint(10, 5000)])
        text = str(value)
    if RNG.random() < 0.25:  # унарный минус перед числом или скобкой
        text, value = "-" + _spaces() + text, -value
    return text, value


def test_evaluate_expression_examples():
    assert evaluate_expression("25 - (6 + (11 - 3)) + 4") == 15
    assert evaluate_expression("7") == 7
    assert evaluate_expression("  120  ") == 120          # многозначное число, пробелы
    assert evaluate_expression("1-2-3") == -4             # слева направо, не 1-(2-3)
    assert evaluate_expression("-5 + 2") == -3            # унарный минус перед числом
    assert evaluate_expression("-(4 - 9)") == 5           # унарный минус перед скобкой
    assert evaluate_expression("10 - (-3)") == 13
    assert evaluate_expression("3 - -2") == 5
    assert evaluate_expression("+8") == 8
    assert evaluate_expression("((((6))))") == 6
    assert evaluate_expression("2-(3-(4-(5-6)))") == 4
    assert evaluate_expression("0") == 0


def test_evaluate_expression_rejects_unknown_symbols():
    with pytest.raises(ValueError):
        evaluate_expression("2 * 3")


def test_evaluate_expression_random():
    allowed = set("0123456789+-() ")
    for _ in range(ROUNDS):
        text, expected = _random_expression(3)
        assert evaluate_expression(text) == expected
        # Вторая, независимая проверка. eval безопасен: строку собрали сами,
        # и в ней нет ничего, кроме цифр, знаков, скобок и пробелов.
        assert set(text) <= allowed
        assert eval(text, {"__builtins__": {}}, {}) == expected


# ---------- repeated_removal_of_adjacent_duplicates ----------

def _removal_brute(text):
    # Буквально по условию: ищем первую пару, вырезаем, начинаем заново.
    while True:
        for i in range(len(text) - 1):
            if text[i] == text[i + 1]:
                text = text[:i] + text[i + 2:]
                break
        else:
            return text


def test_repeated_removal_of_adjacent_duplicates_examples():
    assert repeated_removal_of_adjacent_duplicates("kayyakpop") == "pop"
    assert repeated_removal_of_adjacent_duplicates("abccba") == ""       # цепная реакция
    assert repeated_removal_of_adjacent_duplicates("aaa") == "a"         # три подряд: уходит пара
    assert repeated_removal_of_adjacent_duplicates("aaaa") == ""
    assert repeated_removal_of_adjacent_duplicates("abc") == "abc"
    assert repeated_removal_of_adjacent_duplicates("z") == "z"
    assert repeated_removal_of_adjacent_duplicates("") == ""


def test_repeated_removal_of_adjacent_duplicates_random():
    for _ in range(ROUNDS):
        text = "".join(RNG.choice("abc") for _ in range(RNG.randint(0, 12)))
        assert repeated_removal_of_adjacent_duplicates(text) == _removal_brute(text)


# ---------- implement_a_queue_using_stacks ----------

def test_stack_queue_examples():
    queue = StackQueue()
    assert queue.is_empty() and len(queue) == 0

    queue.enqueue("a")
    queue.enqueue("b")
    assert queue.peek() == "a"
    assert queue.dequeue() == "a"

    # Новый элемент приходит, когда outbox не пуст: он не должен обогнать "b".
    queue.enqueue("c")
    assert len(queue) == 2
    assert queue.dequeue() == "b"
    assert queue.dequeue() == "c"
    assert queue.is_empty()


def test_stack_queue_empty_raises():
    queue = StackQueue()
    with pytest.raises(IndexError):
        queue.dequeue()
    with pytest.raises(IndexError):
        queue.peek()
    queue.enqueue(1)
    queue.dequeue()
    with pytest.raises(IndexError):
        queue.dequeue()


def test_stack_queue_random_against_deque():
    for _ in range(ROUNDS):
        queue, reference = StackQueue(), deque()
        for _ in range(RNG.randint(0, 30)):
            action = RNG.choice(["enqueue", "enqueue", "dequeue", "peek"])
            if action == "enqueue":
                item = RNG.randint(0, 99)
                queue.enqueue(item)
                reference.append(item)
            elif not reference:
                with pytest.raises(IndexError):
                    getattr(queue, action)()
            elif action == "dequeue":
                assert queue.dequeue() == reference.popleft()
            else:
                assert queue.peek() == reference[0]
            assert len(queue) == len(reference)
            assert queue.is_empty() == (not reference)


def test_stack_queue_is_amortized_constant():
    # Если бы элементы перекладывались при каждом dequeue, это было бы O(n^2).
    size = 200_000
    queue = StackQueue()
    for item in range(size):
        queue.enqueue(item)
    assert [queue.dequeue() for _ in range(size)] == list(range(size))


# ---------- maximums_of_sliding_window ----------

def _window_brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def test_maximums_of_sliding_window_examples():
    assert maximums_of_sliding_window([4, 2, 7, 1, 3, 6, 5], 3) == [7, 7, 7, 6, 6]
    assert maximums_of_sliding_window([4, 2, 7], 1) == [4, 2, 7]       # окно из одного
    assert maximums_of_sliding_window([4, 2, 7], 3) == [7]             # окно на весь массив
    assert maximums_of_sliding_window([4, 2, 7], 4) == []              # окно не помещается
    assert maximums_of_sliding_window([5, 5, 5, 5], 2) == [5, 5, 5]
    assert maximums_of_sliding_window([9, 7, 5, 3], 2) == [9, 7, 5]    # убывание: дек растёт
    assert maximums_of_sliding_window([-3, -1, -7], 2) == [-1, -1]
    assert maximums_of_sliding_window([], 2) == []


def test_maximums_of_sliding_window_rejects_bad_size():
    with pytest.raises(ValueError):
        maximums_of_sliding_window([1, 2, 3], 0)


def test_maximums_of_sliding_window_random():
    for _ in range(ROUNDS):
        nums = [RNG.randint(-9, 9) for _ in range(RNG.randint(0, 12))]
        k = RNG.randint(1, 6)
        assert maximums_of_sliding_window(nums, k) == _window_brute(nums, k)


def test_maximums_of_sliding_window_is_linear():
    # Перебор «max по каждому окну» здесь сделал бы 10^10 сравнений.
    size, k = 200_000, 100_000
    descending = list(range(size, 0, -1))
    assert maximums_of_sliding_window(descending, k) == descending[:size - k + 1]

"""Тесты к паттерну Tries.

Структуры данных сверяются с наивным эталоном — обычным множеством строк,
в котором префиксы и шаблоны проверяются перебором всех слов. Поиск слов
на поле сверяется с полным перебором всех путей по клеткам.
"""

import copy
import random

import pytest

from design_a_trie import Trie
from find_all_words_on_a_board import (
    build_word_trie,
    find_all_words_on_a_board,
    search_board,
)
from insert_and_search_words_with_wildcards import WildcardDictionary
from tries_helpers import TrieNode, count_nodes, render_trie

RNG = random.Random(2024)
ROUNDS = 400


def _random_word(alphabet, max_len, min_len=1):
    return "".join(RNG.choice(alphabet) for _ in range(RNG.randint(min_len, max_len)))


# ---------- design_a_trie ----------

def test_trie_examples():
    trie = Trie()
    trie.insert("sung")
    trie.insert("sky")
    assert trie.has_prefix("su")
    assert not trie.search("sun")          # путь есть, слова нет
    trie.insert("sun")
    assert trie.search("sun")
    assert trie.search("sung")
    assert not trie.search("sunga")        # длиннее любого слова
    assert not trie.search("s")
    assert trie.has_prefix("s")
    assert trie.has_prefix("sky")          # слово — префикс самого себя
    assert not trie.has_prefix("sko")
    assert not trie.has_prefix("a")
    assert len(trie) == 3


def test_trie_empty_and_duplicates():
    trie = Trie()
    assert len(trie) == 0
    assert not trie.search("a")
    assert not trie.has_prefix("a")
    assert not trie.has_prefix("")         # слов нет — нет и слов с пустым префиксом

    trie.insert("moon")
    trie.insert("moon")
    assert len(trie) == 1
    assert trie.has_prefix("")
    assert not trie.search("")

    trie.insert("")                        # пустое слово — отметка на корне
    assert trie.search("")
    assert len(trie) == 2


def test_trie_is_not_limited_to_latin_letters():
    trie = Trie()
    trie.insert("ёж")
    trie.insert("ёлка")
    assert trie.has_prefix("ё")
    assert trie.search("ёж")
    assert not trie.search("ёл")


def test_trie_shares_prefixes():
    trie = Trie()
    for word in ["sun", "sung", "sky", "so"]:
        trie.insert(word)
    # s, u, n, g, k, y, o + корень: общая «s» и общая «sun» хранятся один раз.
    assert count_nodes(trie._root) == 8


def test_trie_random_against_set():
    for _ in range(ROUNDS):
        trie = Trie()
        reference: set[str] = set()
        for _ in range(RNG.randint(1, 30)):
            word = _random_word("abc", 5)
            action = RNG.randint(0, 2)
            if action == 0:
                trie.insert(word)
                reference.add(word)
            elif action == 1:
                assert trie.search(word) == (word in reference), (reference, word)
            else:
                expected = any(item.startswith(word) for item in reference)
                assert trie.has_prefix(word) == expected, (reference, word)
        assert len(trie) == len(reference)


# ---------- insert_and_search_words_with_wildcards ----------

def _pattern_fits(pattern, word):
    return len(pattern) == len(word) and all(
        p == "." or p == w for p, w in zip(pattern, word)
    )


def test_wildcards_examples():
    book = WildcardDictionary()
    for word in ["lamp", "lime", "line"]:
        book.insert(word)
    assert book.search("lime")
    assert book.search("li.e")
    assert book.search("l..p")
    assert book.search(".ine")
    assert book.search("....")
    assert not book.search("li.")          # короче любого слова
    assert not book.search(".....")        # длиннее любого слова
    assert not book.search("la.e")         # начало от lamp, конец от lime — не слово
    assert not book.search("lin")          # префикс, но не слово
    assert not book.search(".amb")


def test_wildcards_first_branch_fails_second_succeeds():
    book = WildcardDictionary()
    book.insert("ax")
    book.insert("by")
    # Первая же ветвь под точкой (a) ведёт в тупик — поиск обязан вернуться
    # и попробовать вторую.
    assert book.search(".y")
    assert not book.search(".z")


def test_wildcards_empty():
    book = WildcardDictionary()
    assert not book.search("")
    assert not book.search(".")
    assert not book.search("a")
    book.insert("a")
    assert book.search(".")
    assert not book.search("..")
    assert not book.search("")


def test_wildcards_rejects_dot_in_inserted_word():
    with pytest.raises(ValueError):
        WildcardDictionary().insert("a.b")


def test_wildcards_long_pattern_of_dots():
    # Глубина рекурсии равна числу точек; 300 точек — далеко до лимита.
    book = WildcardDictionary()
    book.insert("z" * 300)
    assert book.search("." * 300)
    assert not book.search("." * 299)
    assert not book.search("." * 299 + "y")


def test_wildcards_random_against_set():
    for _ in range(ROUNDS):
        book = WildcardDictionary()
        reference: set[str] = set()
        for _ in range(RNG.randint(1, 30)):
            if RNG.random() < 0.4:
                word = _random_word("abc", 4)
                book.insert(word)
                reference.add(word)
            else:
                pattern = _random_word("abc...", 4)
                expected = any(_pattern_fits(pattern, word) for word in reference)
                assert book.search(pattern) == expected, (reference, pattern)


# ---------- find_all_words_on_a_board ----------

BOARD = [
    list("pear"),
    list("lint"),
    list("usoe"),
]
WORDS = ["pear", "pea", "pep", "plus", "lint", "line", "ant", "son", "eon"]


def _all_board_strings(board, max_len):
    """Все строки, читаемые на поле по простым путям длиной до max_len."""
    if not board or not board[0]:
        return set()
    rows, cols = len(board), len(board[0])
    strings = set()

    def extend(row, col, used, text):
        strings.add(text)
        if len(text) == max_len:
            return
        for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            cell = (row + d_row, col + d_col)
            if 0 <= cell[0] < rows and 0 <= cell[1] < cols and cell not in used:
                extend(cell[0], cell[1], used | {cell}, text + board[cell[0]][cell[1]])

    for row in range(rows):
        for col in range(cols):
            extend(row, col, {(row, col)}, board[row][col])
    return strings


def _board_brute(board, words):
    max_len = max((len(word) for word in words), default=0)
    readable = _all_board_strings(board, max_len)
    return sorted(set(words) & readable)


def test_board_example():
    board = copy.deepcopy(BOARD)
    answer = find_all_words_on_a_board(board, WORDS)
    # Порядок — порядок обнаружения: из «p» обход сначала идёт вниз, к «plus».
    assert answer == ["plus", "pea", "pear", "ant", "lint", "son", "eon"]
    assert board == BOARD                  # поле восстановлено


def test_board_cell_is_not_reused():
    assert find_all_words_on_a_board([["a", "b"]], ["aba", "abab", "ab", "ba"]) == ["ab", "ba"]
    assert find_all_words_on_a_board([["a"]], ["a", "aa"]) == ["a"]
    # Клетка освобождается при откате: «o» нужна и слову «no», и слову «on».
    assert sorted(find_all_words_on_a_board([["n", "o"]], ["no", "on"])) == ["no", "on"]


def test_board_word_reported_once():
    # «aa» читается восемью способами, а слово в списке ещё и повторяется.
    board = [["a", "a"], ["a", "a"]]
    assert find_all_words_on_a_board(board, ["aa", "aa", "aaaa", "aaaaa"]) == ["aa", "aaaa"]


def test_board_no_diagonals():
    board = [["a", "x"], ["y", "b"]]
    assert sorted(find_all_words_on_a_board(board, ["ab", "ax", "ay"])) == ["ax", "ay"]


def test_board_degenerate_inputs():
    assert find_all_words_on_a_board([], ["a"]) == []
    assert find_all_words_on_a_board([[]], ["a"]) == []
    assert find_all_words_on_a_board([["a"]], []) == []
    assert find_all_words_on_a_board([["a"]], [""]) == []
    # Слово длиннее, чем клеток на поле.
    assert find_all_words_on_a_board([["a", "b"]], ["abc"]) == []


def test_board_pruning_empties_the_trie():
    root = build_word_trie(["pea", "pear", "plus"])
    assert count_nodes(root) == 8         # корень + p,e,a,r + l,u,s
    found, _ = search_board(copy.deepcopy(BOARD), root, prune=True)
    assert found == ["plus", "pea", "pear"]
    # Все слова найдены — от дерева остался один корень.
    assert count_nodes(root) == 1

    # Ненайденное слово остаётся вместе со своей веткой, найденные срезаны.
    root = build_word_trie(["pea", "pear", "pets"])
    search_board(copy.deepcopy(BOARD), root, prune=True)
    assert render_trie(root) == "(root)\n└─ p\n   └─ e\n      └─ t\n         └─ s*"


def test_board_pruning_saves_work():
    # Поле из одинаковых букв — худший случай: без обрезки каждый обход
    # заново проходит по ветке уже найденного слова.
    board = [["a"] * 4 for _ in range(4)]
    words = ["aaaaaa"]
    with_pruning, fast_calls = search_board(board, build_word_trie(words), prune=True)
    without, slow_calls = search_board(board, build_word_trie(words), prune=False)
    assert with_pruning == without == ["aaaaaa"]
    assert fast_calls == 6                 # один спуск до слова — и trie пуст
    assert slow_calls > 100 * fast_calls


def test_board_random_against_brute_force():
    for _ in range(ROUNDS):
        rows, cols = RNG.randint(1, 3), RNG.randint(1, 3)
        board = [[RNG.choice("abc") for _ in range(cols)] for _ in range(rows)]
        words = [_random_word("abc", 5) for _ in range(RNG.randint(0, 8))]
        snapshot = copy.deepcopy(board)
        expected = _board_brute(board, words)

        answer = find_all_words_on_a_board(board, words)
        assert board == snapshot
        assert len(answer) == len(set(answer)), (board, words, answer)
        assert sorted(answer) == expected, (board, words)

        # Обрезка — только ускорение: без неё ответ тот же, работы не меньше.
        plain, slow_calls = search_board(board, build_word_trie(words), prune=False)
        _, fast_calls = search_board(board, build_word_trie(words), prune=True)
        assert sorted(plain) == expected
        assert fast_calls <= slow_calls


# ---------- tries_helpers ----------

def test_render_trie():
    root = TrieNode()
    assert render_trie(root) == "(root)"
    assert count_nodes(root) == 1
    root = build_word_trie(["so", "sky", "s"])
    assert render_trie(root) == "\n".join([
        "(root)",
        "└─ s*",
        "   ├─ k",
        "   │  └─ y*",
        "   └─ o*",
    ])

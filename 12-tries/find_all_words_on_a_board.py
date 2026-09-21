"""Найти на клеточном поле все слова из списка.

Слово складывается из соседних по стороне клеток, клетку нельзя брать
дважды в пределах одного слова. Каждое найденное слово попадает в ответ
один раз.

Приём: trie-guided backtracking. Все слова кладём в один trie и обходим
поле в глубину, спускаясь по trie синхронно с шагами по клеткам: нет ребра
с нужной буквой — ветку перебора бросаем сразу, для всех слов одновременно.
Найденное слово снимаем с trie, а опустевшие узлы срезаем (pruning).
Аналог: LeetCode 212.
"""

from __future__ import annotations

from tries_helpers import TrieNode

# Пустая строка не может быть ребром trie: рёбра — это символы слов.
_VISITED = ""
_STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def build_word_trie(words: list[str]) -> TrieNode:
    """Собрать trie из списка слов. Время и память O(W), W — сумма длин."""
    root = TrieNode()
    for word in words:
        if not word:
            continue  # пустое слово на поле «найти» нельзя — пути длины 0 нет
        node = root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode())
        node.is_word = True
    return root


def find_all_words_on_a_board(board: list[list[str]], words: list[str]) -> list[str]:
    """Вернуть слова из words, которые можно прочитать на поле.

    Порядок ответа — порядок обнаружения. Поле на время обхода помечается,
    но к выходу из функции возвращается в исходное состояние.

    Время O(W + R·C·3^L) в худшем случае: W — сумма длин слов, R×C — размер
    поля, L — длина самого длинного слова (из клетки 4 направления, дальше
    не больше 3, потому что назад нельзя). Память O(W) на trie и O(L) на
    рекурсию.
    """
    found, _ = search_board(board, build_word_trie(words), prune=True)
    return found


def search_board(
    board: list[list[str]], root: TrieNode, prune: bool = True
) -> tuple[list[str], int]:
    """Обойти поле с готовым trie; вернуть найденные слова и число вызовов DFS.

    Trie при обходе меняется: с найденных слов снимается отметка, а при
    prune=True ещё и удаляются опустевшие ветви. Счётчик вызовов и флаг
    prune нужны только затем, чтобы показать, сколько работы экономит обрезка.
    """
    if not board or not board[0]:
        return [], 0

    rows, cols = len(board), len(board[0])
    found: list[str] = []
    path: list[str] = []  # буквы от корня trie до текущего узла
    calls = 0

    def explore(row: int, col: int, parent: TrieNode) -> None:
        nonlocal calls
        calls += 1
        letter = board[row][col]
        node = parent.children[letter]  # вызывающий проверил, что ребро есть
        path.append(letter)

        if node.is_word:
            found.append("".join(path))
            # Снимаем отметку: то же слово, прочитанное другим путём,
            # второй раз в ответ не попадёт. Множество для ответа не нужно.
            node.is_word = False

        board[row][col] = _VISITED
        for d_row, d_col in _STEPS:
            next_row, next_col = row + d_row, col + d_col
            if (
                0 <= next_row < rows
                and 0 <= next_col < cols
                # Помеченная клетка отсеивается этой же проверкой:
                # ребра с пустой строкой в trie не бывает.
                and board[next_row][next_col] in node.children
            ):
                explore(next_row, next_col, node)
        board[row][col] = letter
        path.pop()

        # Обрезка. Узел без отметки и без потомков больше не ведёт ни
        # к одному ненайденному слову — убираем его, чтобы следующие
        # обходы не заходили в тупик. Срезаем на выходе из рекурсии,
        # поэтому опустевшая цепочка схлопывается снизу вверх сама.
        if prune and not node.is_word and not node.children:
            del parent.children[letter]

    for row in range(rows):
        for col in range(cols):
            if not root.children:
                return found, calls  # все слова найдены, искать больше нечего
            if board[row][col] in root.children:
                explore(row, col, root)
    return found, calls

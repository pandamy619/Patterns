"""Словарь с поиском по шаблону: точка заменяет любую одну букву.

Приём: branching DFS. Обычная буква ведёт по единственному ребру, как
в простом trie, а на точке поиск ветвится по всем потомкам узла.
Аналог: LeetCode 211.
"""

from __future__ import annotations

from tries_helpers import TrieNode

WILDCARD = "."


class WildcardDictionary:
    """Память O(W), W — суммарная длина вставленных слов."""

    def __init__(self) -> None:
        self._root = TrieNode()

    def insert(self, word: str) -> None:
        """Добавить слово. Время O(L), L — длина слова."""
        # Точка в самом слове сделала бы поиск двусмысленным: ребро «.»
        # нельзя отличить от шаблона. Лучше отказать сразу.
        if WILDCARD in word:
            raise ValueError("точка допустима только в шаблоне поиска")
        node = self._root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode())
        node.is_word = True

    def search(self, pattern: str) -> bool:
        """Есть ли слово, подходящее под шаблон.

        Время: O(L) без точек; с точками — не больше числа узлов trie
        на первых L уровнях, то есть O(min(A^L, N)), где A — размер
        алфавита, N — число узлов. Память O(L) на стек рекурсии.
        """
        return self._matches(self._root, pattern, 0)

    def _matches(self, node: TrieNode, pattern: str, start: int) -> bool:
        # Буквы проходим циклом, рекурсия нужна только на точках:
        # глубина стека равна числу точек, а не длине шаблона.
        for index in range(start, len(pattern)):
            symbol = pattern[index]
            if symbol == WILDCARD:
                # any() останавливается на первом успехе — остальные ветви
                # не обходим.
                return any(
                    self._matches(child, pattern, index + 1)
                    for child in node.children.values()
                )
            child = node.children.get(symbol)
            if child is None:
                return False
            node = child
        # Шаблон кончился: длина совпала, осталось проверить, что здесь
        # действительно кончается слово, а не проходит чужой префикс.
        return node.is_word

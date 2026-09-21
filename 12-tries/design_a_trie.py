"""Префиксное дерево с тремя операциями: insert, search, has_prefix.

Приём: prefix walk — спуск от корня по одному символу за шаг. Все три
операции отличаются только тем, что делают в конце спуска.
Аналог: LeetCode 208.
"""

from __future__ import annotations

from tries_helpers import TrieNode


class Trie:
    """Множество строк с быстрым ответом на вопрос о префиксе.

    Память O(W) в худшем случае, где W — суммарная длина вставленных слов;
    на практике меньше, потому что общие префиксы хранятся один раз.
    """

    def __init__(self) -> None:
        self._root = TrieNode()
        self._size = 0

    def __len__(self) -> int:
        """Сколько разных слов хранится."""
        return self._size

    def insert(self, word: str) -> None:
        """Добавить слово. Время O(L), L — длина слова; новых узлов не больше L."""
        node = self._root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                child = TrieNode()
                node.children[letter] = child
            node = child
        # Повторная вставка ничего не меняет — это множество, а не счётчик.
        if not node.is_word:
            node.is_word = True
            self._size += 1

    def search(self, word: str) -> bool:
        """Есть ли слово целиком. Время O(L), память O(1)."""
        node = self._walk(word)
        # Дойти до узла мало: «sun» лежит на пути к «sung», даже если само
        # слово «sun» никто не вставлял. Решает отметка конца слова.
        return node is not None and node.is_word

    def has_prefix(self, prefix: str) -> bool:
        """Есть ли слово, начинающееся с prefix. Время O(L), память O(1)."""
        node = self._walk(prefix)
        if node is None:
            return False
        # Удаления нет, поэтому любой узел, кроме корня, создан какой-то
        # вставкой и под ним обязательно лежит слово. Проверка ниже нужна
        # ради корня: у пустого дерева нет слов даже с пустым префиксом.
        return node.is_word or bool(node.children)

    def _walk(self, text: str) -> TrieNode | None:
        """Спуститься по символам text; None, если путь обрывается."""
        node = self._root
        for letter in text:
            node = node.children.get(letter)
            if node is None:
                return None
        return node

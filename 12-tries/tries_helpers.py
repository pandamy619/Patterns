"""Общие детали темы Tries: узел префиксного дерева и две утилиты.

Узел нужен всем трём задачам, поэтому живёт в одном месте. Утилиты
`count_nodes` и `render_trie` в решениях не участвуют: первая помогает
оценивать память и проверять обрезку в тестах, вторая рисует дерево
для трассировок в README.
"""

from __future__ import annotations


class TrieNode:
    """Узел trie: переходы по символам и отметка «здесь кончается слово».

    Сам символ в узле не хранится — он записан на ребре, то есть служит
    ключом в словаре родителя.
    """

    # Узлов в trie много — по одному на символ, — поэтому экономим на каждом:
    # без __slots__ у объекта появляется собственный __dict__.
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        # dict, а не список на 26 ячеек: годится для любого алфавита и не
        # держит пустые ячейки в узлах с одним-двумя потомками.
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False


def count_nodes(root: TrieNode) -> int:
    """Сколько узлов в дереве, считая корень. Время O(число узлов)."""
    total = 0
    stack = [root]
    while stack:
        node = stack.pop()
        total += 1
        stack.extend(node.children.values())
    return total


def render_trie(root: TrieNode) -> str:
    """Нарисовать дерево псевдографикой; звёздочка отмечает конец слова."""
    lines = ["(root)" + ("*" if root.is_word else "")]

    def draw(node: TrieNode, indent: str) -> None:
        letters = sorted(node.children)
        for position, letter in enumerate(letters):
            child = node.children[letter]
            is_last = position == len(letters) - 1
            mark = "*" if child.is_word else ""
            lines.append(f"{indent}{'└─ ' if is_last else '├─ '}{letter}{mark}")
            draw(child, indent + ("   " if is_last else "│  "))

    draw(root, "")
    return "\n".join(lines)

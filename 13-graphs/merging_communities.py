"""Сообщества, которые сливаются: connect(x, y) и get_community_size(x).

Приём: Union-Find (система непересекающихся множеств) с двумя эвристиками —
union by size (меньшее дерево подвешивается к большему) и path compression
(сжатие путей).
Точного аналога на LeetCode нет; та же структура решает LeetCode 547 и 684.
"""


class UnionFind:
    """Лес деревьев: каждое множество — дерево, его корень — представитель.

    find и union — амортизированно O(α(n)), то есть практически O(1).
    Память O(n).
    """

    def __init__(self, count: int) -> None:
        self.parent = list(range(count))    # сначала каждый сам себе корень
        self.size = [1] * count             # верно только для корней

    def find(self, x: int) -> int:
        """Корень дерева, в котором лежит x."""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        # Сжатие путей: всех, кого прошли, подвешиваем прямо к корню,
        # чтобы следующий find по этой ветке был в один шаг. Двумя циклами,
        # а не рекурсией — длинная цепочка не переполнит стек.
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x: int, y: int) -> bool:
        """Слить множества x и y. False, если они уже были одним множеством."""
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False                    # иначе размер удвоился бы на пустом месте
        # Меньшее дерево — под большее: высота растёт, только когда размер
        # хотя бы удваивается, поэтому она не превышает log n.
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def size_of(self, x: int) -> int:
        """Размер множества, в котором лежит x."""
        # Размер хранится у корня; у остальных вершин значение устаревшее.
        return self.size[self.find(x)]


class MergingCommunities:
    """Интерфейс из условия задачи поверх UnionFind."""

    def __init__(self, n: int) -> None:
        self._sets = UnionFind(n)

    def connect(self, x: int, y: int) -> None:
        """Познакомить x и y — их сообщества сливаются. Амортизированно O(α(n))."""
        self._sets.union(x, y)

    def get_community_size(self, x: int) -> int:
        """Сколько людей в сообществе x. Амортизированно O(α(n))."""
        return self._sets.size_of(x)

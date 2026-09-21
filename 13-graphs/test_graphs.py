"""Тесты к теме Graphs.

Кроме ручных примеров каждое решение сверяется с медленным, но очевидно
правильным эталоном на случайных данных: перебор раскрасок, перестановок
и остовных деревьев, посекундная симуляция, Флойд — Уоршелл и т.п.
"""

import random
from itertools import combinations, permutations, product

from bipartite_graph_validation import bipartite_graph_validation
from connect_the_dots import connect_the_dots, connect_the_dots_prim
from count_islands import count_islands
from graph_deep_copy import graph_deep_copy
from graphs_helpers import GraphNode, build_graph, collect_nodes, graph_to_adjacency
from longest_increasing_path import (
    longest_increasing_path,
    longest_increasing_path_iterative,
)
from matrix_infection import matrix_infection
from merging_communities import MergingCommunities, UnionFind
from prerequisites import prerequisites
from shortest_path import shortest_path
from shortest_transformation_sequence import (
    shortest_transformation_sequence,
    shortest_transformation_sequence_bidirectional,
)

RNG = random.Random(2024)
ROUNDS = 300

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _random_matrix(values, max_rows=5, max_cols=5):
    rows, cols = RNG.randint(1, max_rows), RNG.randint(1, max_cols)
    return [[RNG.choice(values) for _ in range(cols)] for _ in range(rows)]


def _grid_neighbors(matrix, r, c):
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
            yield nr, nc


# ---------- graph_deep_copy ----------

def _random_connected_adjacency(size):
    """Случайное дерево плюс несколько лишних рёбер — связный граф с циклами."""
    labels = RNG.sample(range(100), size)
    links = {label: set() for label in labels}
    for index in range(1, size):
        a, b = labels[index], labels[RNG.randrange(index)]
        links[a].add(b)
        links[b].add(a)
    for _ in range(RNG.randint(0, size)):
        a, b = RNG.sample(labels, 2) if size > 1 else (labels[0], labels[0])
        if a != b:
            links[a].add(b)
            links[b].add(a)
    return {label: sorted(neighbors) for label, neighbors in links.items()}


def test_graph_deep_copy_examples():
    assert graph_deep_copy(None) is None

    lonely = GraphNode(7)
    copy = graph_deep_copy(lonely)
    assert copy is not lonely and copy.val == 7 and copy.neighbors == []

    # Квадрат 1-2-3-4 с диагональю 1-3: есть и циклы, и два пути до вершины.
    adjacency = {1: [2, 3, 4], 2: [1, 3], 3: [1, 2, 4], 4: [1, 3]}
    nodes = build_graph(adjacency)
    copy = graph_deep_copy(nodes[1])
    assert copy.val == 1
    assert graph_to_adjacency(copy) == graph_to_adjacency(nodes[1])


def test_graph_deep_copy_self_loop():
    node = GraphNode(5)
    node.neighbors.append(node)
    copy = graph_deep_copy(node)
    assert copy is not node
    assert copy.neighbors == [copy]


def test_graph_deep_copy_random():
    for _ in range(ROUNDS):
        adjacency = _random_connected_adjacency(RNG.randint(1, 8))
        nodes = build_graph(adjacency)
        entry = nodes[RNG.choice(list(adjacency))]
        copy = graph_deep_copy(entry)

        assert copy.val == entry.val
        copied_nodes = collect_nodes(copy)
        # Структура совпадает, порядок соседей сохранён.
        assert {n.val: [x.val for x in n.neighbors] for n in copied_nodes} == adjacency
        # Ни одного общего объекта с оригиналом.
        original_ids = {id(n) for n in nodes.values()}
        assert all(id(n) not in original_ids for n in copied_nodes)
        # На каждое значение — ровно одна копия.
        assert len(copied_nodes) == len(adjacency)


def test_graph_deep_copy_is_independent():
    nodes = build_graph({1: [2], 2: [1]})
    copy = graph_deep_copy(nodes[1])
    copy.neighbors[0].val = 99
    copy.neighbors.clear()
    assert graph_to_adjacency(nodes[1]) == {1: [2], 2: [1]}


# ---------- count_islands ----------

def _count_islands_brute(matrix):
    """Каждой клетке суши — свой номер; соседи перенимают меньший, пока что-то меняется."""
    label = {
        (r, c): r * len(matrix[0]) + c
        for r, row in enumerate(matrix)
        for c, value in enumerate(row)
        if value == 1
    }
    changed = True
    while changed:
        changed = False
        for (r, c) in label:
            for cell in _grid_neighbors(matrix, r, c):
                if cell in label and label[cell] < label[(r, c)]:
                    label[(r, c)] = label[cell]
                    changed = True
    return len(set(label.values()))


def test_count_islands_examples():
    matrix = [
        [1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0],
        [1, 1, 0, 0, 1],
    ]
    assert count_islands(matrix) == 5
    assert count_islands([[1, 0], [0, 1]]) == 2        # диагональ не соединяет
    assert count_islands([[1, 1], [1, 1]]) == 1
    assert count_islands([[0, 0], [0, 0]]) == 0
    assert count_islands([[1]]) == 1
    assert count_islands([]) == 0
    assert count_islands([[]]) == 0


def test_count_islands_random():
    for _ in range(ROUNDS):
        matrix = _random_matrix([0, 1])
        snapshot = [row[:] for row in matrix]
        assert count_islands(matrix) == _count_islands_brute(matrix)
        assert matrix == snapshot, "вход не должен изменяться"


def test_count_islands_huge_single_island():
    # Рекурсивный DFS здесь упал бы с RecursionError.
    assert count_islands([[1] * 300 for _ in range(300)]) == 1


# ---------- matrix_infection ----------

def _matrix_infection_brute(matrix):
    """Честная посекундная симуляция с копией поля на каждом шаге."""
    grid = [row[:] for row in matrix]
    seconds = 0
    while any(1 in row for row in grid):
        following = [row[:] for row in grid]
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if value == 1 and any(grid[nr][nc] == 2 for nr, nc in _grid_neighbors(grid, r, c)):
                    following[r][c] = 2
        if following == grid:
            return -1
        grid = following
        seconds += 1
    return seconds


def test_matrix_infection_examples():
    matrix = [
        [2, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 1, 2],
    ]
    assert matrix_infection(matrix) == 3
    assert matrix_infection([[2, 1, 0, 1]]) == -1      # здоровая клетка за стеной
    assert matrix_infection([[1, 1]]) == -1            # очагов нет, а здоровые есть
    assert matrix_infection([[2, 2], [0, 2]]) == 0     # заражать некого
    assert matrix_infection([[0]]) == 0
    assert matrix_infection([[2, 1, 1, 1, 2]]) == 2    # два очага идут навстречу
    assert matrix_infection([]) == 0


def test_matrix_infection_random():
    for _ in range(ROUNDS):
        matrix = _random_matrix([0, 1, 1, 1, 2])
        snapshot = [row[:] for row in matrix]
        assert matrix_infection(matrix) == _matrix_infection_brute(matrix)
        assert matrix == snapshot, "вход не должен изменяться"


# ---------- bipartite_graph_validation ----------

def _bipartite_brute(graph):
    n = len(graph)
    return any(
        all(coloring[u] != coloring[v] for u in range(n) for v in graph[u])
        for coloring in product((0, 1), repeat=n)
    )


def _random_adjacency_list(n, edge_chance):
    graph = [[] for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if RNG.random() < edge_chance:
            graph[u].append(v)
            graph[v].append(u)
    return graph


def test_bipartite_graph_validation_examples():
    assert bipartite_graph_validation([[1, 3], [0, 2], [1, 3], [0, 2]])             # цикл из 4
    assert not bipartite_graph_validation([[1, 2], [0, 2], [0, 1]])                 # треугольник
    # Две компоненты: ребро 0-1 и треугольник 2-3-4 — обход обязан дойти до второй.
    assert not bipartite_graph_validation([[1], [0], [3, 4], [2, 4], [2, 3]])
    assert bipartite_graph_validation([[], [], []])
    assert bipartite_graph_validation([])
    assert bipartite_graph_validation([[1, 2, 3], [0], [0], [0]])                   # звезда
    assert not bipartite_graph_validation([[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]])  # цикл из 5


def test_bipartite_graph_validation_random():
    for _ in range(ROUNDS):
        n = RNG.randint(0, 8)
        graph = _random_adjacency_list(n, RNG.choice([0.15, 0.3, 0.5]))
        assert bipartite_graph_validation(graph) == _bipartite_brute(graph)


# ---------- longest_increasing_path ----------

def _longest_increasing_path_brute(matrix):
    def walk(r, c):
        return 1 + max(
            (walk(nr, nc) for nr, nc in _grid_neighbors(matrix, r, c)
             if matrix[nr][nc] > matrix[r][c]),
            default=0,
        )

    return max(walk(r, c) for r in range(len(matrix)) for c in range(len(matrix[0])))


def test_longest_increasing_path_examples():
    matrix = [
        [6, 2, 9],
        [7, 3, 8],
        [1, 4, 5],
    ]
    for solve in (longest_increasing_path, longest_increasing_path_iterative):
        assert solve(matrix) == 6                       # 2 -> 3 -> 4 -> 5 -> 8 -> 9
        assert solve([[5, 5], [5, 5]]) == 1             # равные значения путь не продолжают
        assert solve([[42]]) == 1
        assert solve([[1, 2, 3, 4]]) == 4
        assert solve([[3], [2], [1]]) == 3
        assert solve([]) == 0
        assert solve([[]]) == 0


def test_longest_increasing_path_random():
    for _ in range(ROUNDS):
        matrix = _random_matrix(range(1, 10), max_rows=4, max_cols=4)
        expected = _longest_increasing_path_brute(matrix)
        assert longest_increasing_path(matrix) == expected
        assert longest_increasing_path_iterative(matrix) == expected


def test_longest_increasing_path_iterative_long_snake():
    # «Змейка» 100 x 100: путь проходит через все 10 000 клеток.
    size = 100
    matrix = [
        [r * size + (c if r % 2 == 0 else size - 1 - c) for c in range(size)]
        for r in range(size)
    ]
    assert longest_increasing_path_iterative(matrix) == size * size


# ---------- shortest_transformation_sequence ----------

def _transformation_brute(start, end, dictionary):
    """Явный граф попарным сравнением слов + Флойд — Уоршелл."""
    words = list(dict.fromkeys(dictionary))
    if start not in words or end not in words:
        return 0
    n = len(words)
    far = float("inf")
    dist = [[far] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if sum(a != b for a, b in zip(words[i], words[j])) == 1:
                dist[i][j] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    steps = dist[words.index(start)][words.index(end)]
    return 0 if steps == far else steps + 1


SOLVERS = (shortest_transformation_sequence, shortest_transformation_sequence_bidirectional)


def test_shortest_transformation_sequence_examples():
    dictionary = ["cold", "cord", "card", "ward", "warm", "worm", "word", "corm", "bold"]
    for solve in SOLVERS:
        assert solve("cold", "warm", dictionary) == 5    # cold-cord-card-ward-warm
        assert solve("cold", "bold", dictionary) == 2
        assert solve("cold", "cold", dictionary) == 1
        assert solve("cold", "farm", dictionary) == 0    # end нет в словаре
        assert solve("gold", "warm", dictionary) == 0    # start нет в словаре
        assert solve("ab", "cd", ["ab", "cd"]) == 0      # оба есть, но моста нет
        assert solve("a", "c", ["a", "b", "c"]) == 2     # напрямую, а не через b
        assert solve("a", "b", []) == 0


def test_shortest_transformation_sequence_random():
    for _ in range(ROUNDS):
        length = RNG.randint(1, 3)
        pool = ["".join(w) for w in product("abc", repeat=length)]
        dictionary = RNG.sample(pool, RNG.randint(1, min(len(pool), 10)))
        start = RNG.choice(dictionary if RNG.random() < 0.9 else pool)
        end = RNG.choice(dictionary if RNG.random() < 0.9 else pool)
        expected = _transformation_brute(start, end, dictionary)
        for solve in SOLVERS:
            assert solve(start, end, dictionary) == expected


def test_shortest_transformation_sequence_does_not_mutate_input():
    dictionary = ["dog", "dot", "cot"]
    for solve in SOLVERS:
        assert solve("dog", "cot", dictionary) == 3
        assert dictionary == ["dog", "dot", "cot"]


# ---------- merging_communities ----------

class _NaiveCommunities:
    """Эталон: у каждого человека метка сообщества, слияние — перекраска за O(n)."""

    def __init__(self, n):
        self.label = list(range(n))

    def connect(self, x, y):
        old, new = self.label[x], self.label[y]
        self.label = [new if value == old else value for value in self.label]

    def get_community_size(self, x):
        return self.label.count(self.label[x])


def test_merging_communities_examples():
    town = MergingCommunities(6)
    assert town.get_community_size(4) == 1
    town.connect(0, 3)
    town.connect(4, 5)
    assert town.get_community_size(3) == 2
    town.connect(3, 5)
    assert [town.get_community_size(x) for x in range(6)] == [4, 1, 1, 4, 4, 4]
    town.connect(0, 4)                  # уже вместе — размер не должен удвоиться
    town.connect(2, 2)                  # знакомство с самим собой
    assert town.get_community_size(0) == 4
    assert town.get_community_size(2) == 1


def test_merging_communities_random():
    for _ in range(ROUNDS):
        n = RNG.randint(1, 12)
        fast, naive = MergingCommunities(n), _NaiveCommunities(n)
        for _ in range(RNG.randint(0, 30)):
            x, y = RNG.randrange(n), RNG.randrange(n)
            if RNG.random() < 0.5:
                fast.connect(x, y)
                naive.connect(x, y)
            else:
                assert fast.get_community_size(x) == naive.get_community_size(x)
        assert [fast.get_community_size(x) for x in range(n)] == [
            naive.get_community_size(x) for x in range(n)
        ]


def test_union_find_long_chain_is_fast_and_compressed():
    n = 200_000
    sets = UnionFind(n)
    for x in range(n - 1):
        assert sets.union(x, x + 1)
    assert not sets.union(0, n - 1)
    assert sets.size_of(n // 2) == n
    # После find вершина висит прямо на корне — сжатие путей сработало.
    for x in (0, n // 2, n - 1):
        root = sets.find(x)
        assert sets.parent[x] == root


# ---------- prerequisites ----------

def _prerequisites_brute(n, pairs):
    """Перебор всех порядков прохождения курсов."""
    for order in permutations(range(n)):
        position = {course: index for index, course in enumerate(order)}
        if all(position[a] < position[b] for a, b in pairs):
            return True
    return False


def test_prerequisites_examples():
    assert prerequisites(4, [[0, 1], [0, 2], [1, 3], [2, 3]])        # ромб
    assert not prerequisites(4, [[0, 1], [1, 2], [2, 3], [3, 1]])    # цикл 1-2-3
    assert not prerequisites(2, [[0, 1], [1, 0]])
    assert prerequisites(3, [])
    assert prerequisites(0, [])
    assert prerequisites(1, [])
    assert prerequisites(3, [[0, 1], [0, 1], [1, 2]])                # повтор пары
    assert not prerequisites(5, [[0, 1], [2, 3], [3, 4], [4, 2]])    # цикл в отдельной компоненте


def test_prerequisites_random():
    for _ in range(ROUNDS):
        n = RNG.randint(1, 6)
        pairs = []
        for _ in range(RNG.randint(0, 7)):
            a, b = RNG.randrange(n), RNG.randrange(n)
            if a != b:
                pairs.append([a, b])
        assert prerequisites(n, pairs) == _prerequisites_brute(n, pairs)


# ---------- shortest_path ----------

def _shortest_path_brute(n, edges, start):
    """Беллман — Форд: n - 1 раз расслабляем все рёбра подряд."""
    far = float("inf")
    dist = [far] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            dist[v] = min(dist[v], dist[u] + w)
            dist[u] = min(dist[u], dist[v] + w)
    return [-1 if d == far else d for d in dist]


def test_shortest_path_examples():
    edges = [[0, 1, 7], [0, 2, 2], [2, 1, 3], [1, 3, 1], [2, 3, 8], [3, 4, 5]]
    assert shortest_path(6, edges, 0) == [0, 5, 2, 6, 11, -1]
    assert shortest_path(6, edges, 5) == [-1, -1, -1, -1, -1, 0]
    assert shortest_path(1, [], 0) == [0]
    assert shortest_path(3, [], 1) == [-1, 0, -1]
    assert shortest_path(2, [[0, 1, 9], [1, 0, 4]], 0) == [0, 4]          # кратные рёбра
    assert shortest_path(3, [[0, 1, 0], [1, 2, 0], [0, 0, 5]], 2) == [0, 0, 0]  # нулевые веса и петля


def test_shortest_path_random():
    for _ in range(ROUNDS):
        n = RNG.randint(1, 8)
        edges = [
            [RNG.randrange(n), RNG.randrange(n), RNG.randint(0, 9)]
            for _ in range(RNG.randint(0, 12))
        ]
        start = RNG.randrange(n)
        assert shortest_path(n, edges, start) == _shortest_path_brute(n, edges, start)


# ---------- connect_the_dots ----------

def _connect_the_dots_brute(points):
    """Перебор всех наборов из n - 1 ребра; годятся те, что связывают все точки."""
    n = len(points)
    if n <= 1:
        return 0
    edges = [
        (abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
        for i, j in combinations(range(n), 2)
    ]
    best = None
    for chosen in combinations(edges, n - 1):
        reached = {0}
        grew = True
        while grew:
            grew = False
            for _, i, j in chosen:
                if (i in reached) != (j in reached):
                    reached |= {i, j}
                    grew = True
        if len(reached) == n:
            cost = sum(edge[0] for edge in chosen)
            best = cost if best is None else min(best, cost)
    return best


def test_connect_the_dots_examples():
    points = [[0, 0], [1, 3], [4, 0], [5, 4], [2, 1]]
    for solve in (connect_the_dots, connect_the_dots_prim):
        assert solve(points) == 14
        assert solve([]) == 0
        assert solve([[3, 3]]) == 0
        assert solve([[-2, 5], [1, 1]]) == 7
        assert solve([[1, 1], [1, 1], [1, 1]]) == 0        # совпадающие точки
        assert solve([[0, 0], [0, 5], [0, 2]]) == 5        # точки на одной прямой


def test_connect_the_dots_random():
    for _ in range(ROUNDS):
        points = [
            [RNG.randint(-6, 6), RNG.randint(-6, 6)] for _ in range(RNG.randint(0, 6))
        ]
        expected = _connect_the_dots_brute(points)
        assert connect_the_dots(points) == expected
        assert connect_the_dots_prim(points) == expected


def test_connect_the_dots_kruskal_matches_prim_on_larger_input():
    for _ in range(20):
        points = [[RNG.randint(-50, 50), RNG.randint(-50, 50)] for _ in range(60)]
        assert connect_the_dots(points) == connect_the_dots_prim(points)

"""Тесты к паттерну Trees.

Кроме ручных примеров каждое решение сверяется с медленным, но очевидно
правильным эталоном на случайных деревьях. Многие эталоны опираются на
«развёрнутые» уровни: дерево раскладывается в полные ряды длиной 1, 2, 4, ...
с None на пустых местах — в таком виде зеркальность, ширина и симметрия
проверяются буквально по определению.
"""

import random
from collections import defaultdict

import pytest

from balanced_binary_tree_validation import balanced_binary_tree_validation
from binary_search_tree_validation import (
    binary_search_tree_validation,
    binary_search_tree_validation_inorder,
)
from binary_tree_columns import binary_tree_columns
from binary_tree_symmetry import binary_tree_symmetry, binary_tree_symmetry_iterative
from build_binary_tree_from_preorder_and_inorder import (
    build_binary_tree_from_preorder_and_inorder,
)
from invert_binary_tree import invert_binary_tree, invert_binary_tree_iterative
from lowest_common_ancestor import lowest_common_ancestor
from maximum_path_sum_in_a_binary_tree import maximum_path_sum_in_a_binary_tree
from rightmost_nodes_of_a_binary_tree import (
    rightmost_nodes_dfs,
    rightmost_nodes_of_a_binary_tree,
)
from trees_helpers import TreeNode, build_tree, find_node, to_level_list
from widest_binary_tree_level import widest_binary_tree_level

RNG = random.Random(2024)
ROUNDS = 400
DEEP = 50_000  # заведомо больше лимита рекурсии Python


# ---------- общие инструменты ----------

def _random_tree(max_nodes=9, values=None, unique=False):
    """Случайное дерево: каждый новый узел «падает» от корня, выбирая
    сторону монеткой, пока не найдёт свободное место. Формы получаются
    разные — от почти полных до цепочек."""
    size = RNG.randint(0, max_nodes)
    if unique:
        pool = RNG.sample(range(-50, 50), size)
    else:
        pool = [RNG.choice(values or range(-9, 10)) for _ in range(size)]
    root = None
    for value in pool:
        fresh = TreeNode(value)
        if root is None:
            root = fresh
            continue
        node = root
        while True:
            side = RNG.choice(("left", "right"))
            child = getattr(node, side)
            if child is None:
                setattr(node, side, fresh)
                break
            node = child
    return root


def _nodes(root):
    found, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        found.append(node)
        stack.extend(child for child in (node.left, node.right) if child)
    return found


def _padded_levels(root):
    """Полные ряды узлов: ряд d имеет длину 2**d, пустые места — None."""
    levels, row = [], [root]
    while any(row):
        levels.append(row)
        row = [
            child
            for node in row
            for child in ((node.left, node.right) if node else (None, None))
        ]
    return levels


def _padded_values(root):
    return [[node.val if node else None for node in row] for row in _padded_levels(root)]


def _chain(length, side):
    """Вырожденное дерево-«палка» из значений 0..length-1."""
    root = tail = TreeNode(0)
    for value in range(1, length):
        fresh = TreeNode(value)
        setattr(tail, side, fresh)
        tail = fresh
    return root


# ---------- trees_helpers ----------

def test_helpers_round_trip():
    for values in ([], [1], [5, 2, 8, None, 3], [1, None, 2, None, 3], [1, 2, 3, 4, 5, 6, 7]):
        assert to_level_list(build_tree(values)) == values
    root = build_tree([5, 2, 8, None, 3])
    assert root.left.right.val == 3 and root.left.left is None
    assert find_node(root, 8) is root.right
    assert find_node(root, 100) is None
    assert build_tree([None]) is None


def test_helpers_random_round_trip():
    for _ in range(ROUNDS):
        root = _random_tree()
        clone = build_tree(to_level_list(root))
        assert _padded_values(clone) == _padded_values(root)


# ---------- invert_binary_tree ----------

INVERTERS = [invert_binary_tree, invert_binary_tree_iterative]


@pytest.mark.parametrize("invert", INVERTERS)
def test_invert_binary_tree_examples(invert):
    assert to_level_list(invert(build_tree([6, 2, 9, 1, None, 7]))) == [6, 9, 2, None, 7, None, 1]
    assert to_level_list(invert(build_tree([1, 2]))) == [1, None, 2]
    assert to_level_list(invert(build_tree([4]))) == [4]
    assert invert(None) is None
    root = build_tree([1, 2, 3])
    assert invert(root) is root          # меняем на месте, корень тот же


@pytest.mark.parametrize("invert", INVERTERS)
def test_invert_binary_tree_random(invert):
    for _ in range(ROUNDS):
        root = _random_tree()
        expected = [row[::-1] for row in _padded_values(root)]
        assert _padded_values(invert(root)) == expected


def test_invert_binary_tree_iterative_survives_deep_tree():
    root = invert_binary_tree_iterative(_chain(DEEP, "left"))
    assert root.left is None and root.right.val == 1
    with pytest.raises(RecursionError):
        invert_binary_tree(_chain(DEEP, "left"))


# ---------- balanced_binary_tree_validation ----------

def _height_brute(node):
    return 0 if node is None else 1 + max(_height_brute(node.left), _height_brute(node.right))


def _balanced_brute(root):
    return all(
        abs(_height_brute(node.left) - _height_brute(node.right)) <= 1
        for node in _nodes(root)
    )


def test_balanced_binary_tree_validation_examples():
    assert balanced_binary_tree_validation(None)
    assert balanced_binary_tree_validation(build_tree([1]))
    assert balanced_binary_tree_validation(build_tree([4, 2, 7, 1, None, None, 9]))
    assert not balanced_binary_tree_validation(build_tree([1, 2, None, 3]))
    # Корень выглядит ровно (высоты 3 и 3), перекос спрятан внутри поддеревьев.
    hidden = build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7])
    assert not balanced_binary_tree_validation(hidden)


def test_balanced_binary_tree_validation_random():
    seen = set()
    for _ in range(ROUNDS):
        root = _random_tree(max_nodes=7)
        expected = _balanced_brute(root)
        seen.add(expected)
        assert balanced_binary_tree_validation(root) == expected
    assert seen == {True, False}


# ---------- rightmost_nodes_of_a_binary_tree ----------

VIEWERS = [rightmost_nodes_of_a_binary_tree, rightmost_nodes_dfs]


@pytest.mark.parametrize("view", VIEWERS)
def test_rightmost_nodes_examples(view):
    assert view(build_tree([3, 8, 5, 1, 6, None, None, None, None, 4])) == [3, 5, 6, 4]
    assert view(build_tree([1, 2, None, 3])) == [1, 2, 3]    # справа пусто — видно левые
    assert view(build_tree([7])) == [7]
    assert view(None) == []


@pytest.mark.parametrize("view", VIEWERS)
def test_rightmost_nodes_random(view):
    for _ in range(ROUNDS):
        root = _random_tree()
        expected = [
            [value for value in row if value is not None][-1]
            for row in _padded_values(root)
        ]
        assert view(root) == expected


def test_rightmost_nodes_bfs_survives_deep_tree():
    assert rightmost_nodes_of_a_binary_tree(_chain(DEEP, "left")) == list(range(DEEP))


# ---------- widest_binary_tree_level ----------

def _width_brute(root):
    best = 0
    for row in _padded_levels(root):
        occupied = [index for index, node in enumerate(row) if node]
        best = max(best, occupied[-1] - occupied[0] + 1)
    return best


def test_widest_binary_tree_level_examples():
    assert widest_binary_tree_level(None) == 0
    assert widest_binary_tree_level(build_tree([1])) == 1
    assert widest_binary_tree_level(build_tree([1, 2, 3])) == 2
    # Нижний уровень: узлы только по краям, но дырки между ними считаются.
    assert widest_binary_tree_level(build_tree([1, 2, 3, 4, None, None, 5])) == 4
    # Самый широкий уровень — не обязательно последний.
    assert widest_binary_tree_level(build_tree([1, 2, 3, 4, None, None, 5, 6])) == 4
    # Один узел на уровне даёт ширину 1, как бы далеко от оси он ни стоял.
    assert widest_binary_tree_level(build_tree([1, None, 2, None, 3])) == 1


def test_widest_binary_tree_level_random():
    for _ in range(ROUNDS):
        root = _random_tree()
        assert widest_binary_tree_level(root) == _width_brute(root)


def test_widest_binary_tree_level_survives_deep_tree():
    # Без сдвига нумерации позиции здесь доросли бы до 2**50000.
    assert widest_binary_tree_level(_chain(DEEP, "right")) == 1


# ---------- binary_search_tree_validation ----------

BST_CHECKERS = [binary_search_tree_validation, binary_search_tree_validation_inorder]


def _subtree_values(node):
    return [item.val for item in _nodes(node)]


def _bst_brute(root):
    return all(
        all(value < node.val for value in _subtree_values(node.left))
        and all(value > node.val for value in _subtree_values(node.right))
        for node in _nodes(root)
    )


@pytest.mark.parametrize("check", BST_CHECKERS)
def test_binary_search_tree_validation_examples(check):
    assert check(None)
    assert check(build_tree([10]))
    assert check(build_tree([10, 4, 15, 2, 7, 12, 20]))
    # 11 больше своего родителя 7 — локально всё хорошо, но он в ЛЕВОМ поддереве 10.
    assert not check(build_tree([10, 4, 15, 2, 11]))
    assert not check(build_tree([10, 4, 15, None, None, 9]))
    assert not check(build_tree([5, 5]))                # дубликат слева
    assert not check(build_tree([5, None, 5]))          # дубликат справа
    assert check(build_tree([0, -1]))                   # ноль не должен сойти за «нет границы»


@pytest.mark.parametrize("check", BST_CHECKERS)
def test_binary_search_tree_validation_random(check):
    seen = set()
    for _ in range(ROUNDS):
        root = _random_tree(max_nodes=5, values=range(0, 7))
        if RNG.random() < 0.5:
            # Случайное дерево почти никогда не BST, поэтому половину раундов
            # раскладываем отсортированные значения по той же форме (inorder) —
            # получается корректное BST, которое иногда портим одной заменой.
            ordered = sorted(RNG.sample(range(0, 30), len(_nodes(root))))
            _fill_inorder(root, iter(ordered))
            if root and RNG.random() < 0.4:
                RNG.choice(_nodes(root)).val = RNG.randint(0, 30)
        expected = _bst_brute(root)
        seen.add(expected)
        assert check(root) == expected
    assert seen == {True, False}


def _fill_inorder(node, values):
    if node:
        _fill_inorder(node.left, values)
        node.val = next(values)
        _fill_inorder(node.right, values)


def test_binary_search_tree_validation_inorder_survives_deep_tree():
    assert binary_search_tree_validation_inorder(_chain(DEEP, "right"))
    assert not binary_search_tree_validation_inorder(_chain(DEEP, "left"))


# ---------- lowest_common_ancestor ----------

def _lca_brute(root, first, second):
    parent = {root: None}
    for node in _nodes(root):
        for child in (node.left, node.right):
            if child:
                parent[child] = node

    def path_to_root(node):
        path = []
        while node:
            path.append(node)
            node = parent[node]
        return path

    ancestors = path_to_root(first)
    # Первый же предок second, входящий в цепочку предков first, — самый глубокий общий.
    return next(node for node in path_to_root(second) if any(node is a for a in ancestors))


def test_lowest_common_ancestor_examples():
    root = build_tree([8, 3, 12, 1, 6, None, 14, None, None, 4, 7])
    pick = lambda value: find_node(root, value)
    assert lowest_common_ancestor(root, pick(4), pick(7)) is pick(6)
    assert lowest_common_ancestor(root, pick(1), pick(7)) is pick(3)
    assert lowest_common_ancestor(root, pick(4), pick(14)) is root
    assert lowest_common_ancestor(root, pick(3), pick(4)) is pick(3)    # один — предок другого
    assert lowest_common_ancestor(root, pick(7), pick(1)) is pick(3)    # порядок аргументов не важен
    assert lowest_common_ancestor(root, root, pick(14)) is root


def test_lowest_common_ancestor_compares_nodes_not_values():
    root = build_tree([1, 2, 2, 5, None, None, 5])
    assert lowest_common_ancestor(root, root.left.left, root.right.right) is root
    assert lowest_common_ancestor(root, root.left, root.left.left) is root.left


def test_lowest_common_ancestor_random():
    rounds = 0
    while rounds < ROUNDS:
        root = _random_tree(max_nodes=10)
        nodes = _nodes(root)
        if len(nodes) < 2:
            continue
        rounds += 1
        first, second = RNG.sample(nodes, 2)
        assert lowest_common_ancestor(root, first, second) is _lca_brute(root, first, second)


# ---------- build_binary_tree_from_preorder_and_inorder ----------

def _preorder(node):
    return [node.val] + _preorder(node.left) + _preorder(node.right) if node else []


def _inorder(node):
    return _inorder(node.left) + [node.val] + _inorder(node.right) if node else []


def _build_brute(preorder, inorder):
    """Классический вариант со срезами и линейным поиском: O(n^2), зато очевидный."""
    if not preorder:
        return None
    middle = inorder.index(preorder[0])
    return TreeNode(
        preorder[0],
        _build_brute(preorder[1:middle + 1], inorder[:middle]),
        _build_brute(preorder[middle + 1:], inorder[middle + 1:]),
    )


def test_build_binary_tree_examples():
    build = build_binary_tree_from_preorder_and_inorder
    assert to_level_list(build([7, 2, 1, 5, 9, 8], [1, 2, 5, 7, 8, 9])) == [7, 2, 9, 1, 5, 8]
    assert to_level_list(build([1, 2, 3], [3, 2, 1])) == [1, 2, None, 3]          # цепочка влево
    assert to_level_list(build([1, 2, 3], [1, 2, 3])) == [1, None, 2, None, 3]    # цепочка вправо
    assert to_level_list(build([4], [4])) == [4]
    assert build([], []) is None


def test_build_binary_tree_rejects_bad_input():
    build = build_binary_tree_from_preorder_and_inorder
    with pytest.raises(ValueError):
        build([1, 2], [1])
    with pytest.raises(ValueError):
        build([1, 1], [1, 1])


def test_build_binary_tree_random():
    for _ in range(ROUNDS):
        original = _random_tree(max_nodes=10, unique=True)
        preorder, inorder = _preorder(original), _inorder(original)
        rebuilt = build_binary_tree_from_preorder_and_inorder(preorder, inorder)
        assert to_level_list(rebuilt) == to_level_list(original)
        assert to_level_list(rebuilt) == to_level_list(_build_brute(preorder, inorder))


def test_build_binary_tree_is_linear_on_wide_input():
    # Сбалансированное дерево на 2**16 - 1 узлов: вариант со срезами и index()
    # на таком входе заметно медленнее, а глубина рекурсии всего 16.
    size = 2 ** 16 - 1
    inorder = list(range(size))

    def preorder_of(low, high):
        order, stack = [], [(low, high)]
        while stack:
            low, high = stack.pop()
            if low > high:
                continue
            middle = (low + high) // 2
            order.append(middle)
            stack.append((middle + 1, high))
            stack.append((low, middle - 1))
        return order

    root = build_binary_tree_from_preorder_and_inorder(preorder_of(0, size - 1), inorder)
    assert root.val == size // 2
    assert widest_binary_tree_level(root) == 2 ** 15


# ---------- maximum_path_sum_in_a_binary_tree ----------

def _path_sum_brute(root):
    """Дерево как неориентированный граф: из каждого узла идём во все стороны.
    Между двумя узлами дерева путь единственный, так что переберём все пути."""
    if root is None:
        return 0
    neighbours = defaultdict(list)
    for node in _nodes(root):
        for child in (node.left, node.right):
            if child:
                neighbours[node].append(child)
                neighbours[child].append(node)
    best = root.val
    for start in _nodes(root):
        stack = [(start, None, start.val)]
        while stack:
            node, came_from, total = stack.pop()
            best = max(best, total)
            for other in neighbours[node]:
                if other is not came_from:
                    stack.append((other, node, total + other.val))
    return best


def test_maximum_path_sum_examples():
    solve = maximum_path_sum_in_a_binary_tree
    assert solve(build_tree([2, 7, -4, 3, -6, 5, 1])) == 13          # 3 + 7 + 2 + (-4) + 5
    assert solve(build_tree([-5, 4, 6, 3, 2])) == 9                  # 3 + 4 + 2, арка ниже корня
    assert solve(build_tree([-3, -8, -1])) == -1                     # все отрицательные
    assert solve(build_tree([9])) == 9
    assert solve(build_tree([1, 2, 3])) == 6
    assert solve(build_tree([5, -2, None, 10])) == 13                # через отрицательный узел
    assert solve(None) == 0


def test_maximum_path_sum_random():
    for _ in range(ROUNDS):
        root = _random_tree(max_nodes=10)
        assert maximum_path_sum_in_a_binary_tree(root) == _path_sum_brute(root)


# ---------- binary_tree_columns ----------

def _columns_brute(root):
    """Каждому узлу — тройка (столбец, глубина, позиция в полном ряду),
    затем честная сортировка. Позиция в ряду и есть порядок «слева направо»."""
    records = []

    def walk(node, column, depth, slot):
        if node:
            records.append((column, depth, slot, node.val))
            walk(node.left, column - 1, depth + 1, 2 * slot)
            walk(node.right, column + 1, depth + 1, 2 * slot + 1)

    walk(root, 0, 0, 0)
    grouped = defaultdict(list)
    for column, _, _, value in sorted(records, key=lambda record: record[:3]):
        grouped[column].append(value)
    return [grouped[column] for column in sorted(grouped)]


def test_binary_tree_columns_examples():
    assert binary_tree_columns(None) == []
    assert binary_tree_columns(build_tree([1])) == [[1]]
    assert binary_tree_columns(build_tree([1, 2, 3])) == [[2], [1], [3]]
    # 6 и 7 стоят в одной клетке (столбец 0, глубина 2): левый идёт первым,
    # хотя его значение могло бы быть и больше.
    assert binary_tree_columns(build_tree([4, 2, 9, 1, 7, 6, 5])) == [[1], [2], [4, 7, 6], [9], [5]]
    # В столбце 1 встречаются глубокий узел 8 из левого поддерева и мелкий 5
    # из правого: DFS «сначала влево» записал бы 8 раньше 5.
    tricky = build_tree([1, 2, 5, None, 4, 3, None, None, 8])
    assert binary_tree_columns(tricky) == [[2], [1, 4, 3], [5, 8]]


def test_binary_tree_columns_random():
    for _ in range(ROUNDS):
        root = _random_tree(max_nodes=12)
        assert binary_tree_columns(root) == _columns_brute(root)


def test_binary_tree_columns_survives_deep_tree():
    columns = binary_tree_columns(_chain(DEEP, "left"))
    assert columns[0] == [DEEP - 1] and columns[-1] == [0] and len(columns) == DEEP


# ---------- binary_tree_symmetry ----------

SYMMETRY_CHECKERS = [binary_tree_symmetry, binary_tree_symmetry_iterative]


def _symmetry_brute(root):
    return all(row == row[::-1] for row in _padded_values(root))


@pytest.mark.parametrize("check", SYMMETRY_CHECKERS)
def test_binary_tree_symmetry_examples(check):
    assert check(None)
    assert check(build_tree([1]))
    assert check(build_tree([5, 3, 3, 1, 8, 8, 1]))
    assert check(build_tree([5, 3, 3, None, 8, 8]))
    assert not check(build_tree([5, 3, 3, 1, 8, 1, 8]))          # значения не зеркальны
    # Значения по уровням читаются как палиндром, но форма не зеркальна.
    assert not check(build_tree([5, 3, 3, None, 8, None, 8]))
    assert not check(build_tree([1, 2]))


@pytest.mark.parametrize("check", SYMMETRY_CHECKERS)
def test_binary_tree_symmetry_random(check):
    seen = set()
    for _ in range(ROUNDS):
        root = _random_tree(max_nodes=6, values=(1, 2))
        if root and RNG.random() < 0.5:
            # Чисто случайное дерево симметрично редко — делаем половину такими
            # принудительно: правое поддерево := зеркальная копия левого.
            root.right = _mirror_copy(root.left)
            if RNG.random() < 0.3 and root.right:
                RNG.choice(_nodes(root.right)).val = 3       # и иногда ломаем
        expected = _symmetry_brute(root)
        seen.add(expected)
        assert check(root) == expected
    assert seen == {True, False}


def _mirror_copy(node):
    if node is None:
        return None
    return TreeNode(node.val, _mirror_copy(node.right), _mirror_copy(node.left))

"""Завдання 1: найменше значення у двійковому дереві пошуку / AVL-дереві."""

from avl_tree import build_tree


def find_min(root):
    """Повертає найменший ключ дерева або None для порожнього дерева.

    У дереві пошуку найменше значення завжди лежить у крайньому лівому вузлі,
    тому достатньо йти ліворуч, доки є лівий нащадок. Складність O(h),
    для AVL-дерева h = O(log n).
    """
    if root is None:
        return None
    node = root
    while node.left is not None:
        node = node.left
    return node.key


if __name__ == "__main__":
    keys = [10, 20, 30, 25, 28, 27, -1, 5, 3]
    root = build_tree(keys)
    print("AVL-дерево:")
    print(root)
    print("Найменше значення:", find_min(root))

    assert find_min(root) == min(keys)
    assert find_min(None) is None

"""Завдання 2: сума всіх значень у двійковому дереві пошуку / AVL-дереві."""

from avl_tree import build_tree


def sum_values(root):
    """Повертає суму всіх ключів дерева (0 для порожнього дерева).

    Обходимо всі вузли рекурсивно: значення вузла + сума лівого піддерева
    + сума правого піддерева. Складність O(n).
    """
    if root is None:
        return 0
    return root.key + sum_values(root.left) + sum_values(root.right)


if __name__ == "__main__":
    keys = [10, 20, 30, 25, 28, 27, -1, 5, 3]
    root = build_tree(keys)
    print("AVL-дерево:")
    print(root)
    print("Сума всіх значень:", sum_values(root))

    assert sum_values(root) == sum(keys)
    assert sum_values(None) == 0

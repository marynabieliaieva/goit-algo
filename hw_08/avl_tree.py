"""AVL-дерево (реалізація на основі конспекту) з операцією вставки."""


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def get_height(node):
    return node.height if node else 0


def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def _update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def left_rotate(z):
    y = z.right
    t2 = y.left
    y.left = z
    z.right = t2
    _update_height(z)
    _update_height(y)
    return y


def right_rotate(y):
    x = y.left
    t3 = x.right
    x.right = y
    y.left = t3
    _update_height(y)
    _update_height(x)
    return x


def insert(root, key):
    """Вставляє ключ у AVL-дерево й повертає новий корінь піддерева."""
    if root is None:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root  # дублікати не додаємо

    _update_height(root)
    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:  # LL
            return right_rotate(root)
        root.left = left_rotate(root.left)  # LR
        return right_rotate(root)

    if balance < -1:
        if key > root.right.key:  # RR
            return left_rotate(root)
        root.right = right_rotate(root.right)  # RL
        return left_rotate(root)

    return root


def build_tree(keys):
    root = None
    for key in keys:
        root = insert(root, key)
    return root

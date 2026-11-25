"""Завдання 5. Візуалізація обходу бінарного дерева в глибину (DFS, стек) і в ширину (BFS, черга).

Кожен відвіданий вузол отримує унікальний колір у форматі #RRGGBB:
від темного (перший відвіданий) до світлого (останній).
"""

import heapq
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt

from task4_heap_visualization import heap_to_tree
from tree_viz import draw_tree

DARK = (0x0B, 0x1E, 0x3F)   # темно-синій
LIGHT = (0xBF, 0xE6, 0xFF)  # світло-блакитний


def gradient(n):
    """Список із n кольорів #RRGGBB від темного до світлого."""
    colors = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        r, g, b = (round(d + (l - d) * t) for d, l in zip(DARK, LIGHT))
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def count_nodes(root):
    count, stack = 0, [root] if root else []
    while stack:
        node = stack.pop()
        count += 1
        stack.extend(child for child in (node.left, node.right) if child)
    return count


def dfs_order(root):
    """Обхід у глибину (pre-order) за допомогою стека, без рекурсії."""
    order, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        order.append(node)
        # правий кладемо першим, щоб лівий дістали раніше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_order(root):
    """Обхід у ширину за допомогою черги, без рекурсії."""
    order, queue = [], deque([root] if root else [])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


def color_traversal(order):
    """Фарбує вузли у порядку обходу і повертає список (значення, колір)."""
    colors = gradient(len(order))
    for node, color in zip(order, colors):
        node.color = color
    return [(node.val, node.color) for node in order]


def show_steps(build_root, traversal, name, save_path=None):
    """Покроково: на кроці k пофарбовано перші k відвіданих вузлів, решта — сірі."""
    root = build_root()
    order = traversal(root)
    colors = gradient(len(order))
    steps = len(order)
    cols = 4
    rows = (steps + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.5 * cols, 3.6 * rows))
    axes = axes.flatten()
    for k in range(steps):
        for i, node in enumerate(order):
            node.color = colors[i] if i <= k else "#D3D3D3"
        draw_tree(root, title=f"{name}: крок {k + 1} — вузол {order[k].val}", ax=axes[k], node_size=900)
    for ax in axes[steps:]:
        ax.axis("off")
    fig.suptitle(f"{name}: порядок {' → '.join(str(n.val) for n in order)}", fontsize=14)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=80, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    data = [10, 4, 15, 1, 7, 3, 20, 8, 2]
    heapq.heapify(data)

    def build():
        return heap_to_tree(data)

    Path("images").mkdir(exist_ok=True)

    for name, traversal, fname in (("DFS (стек)", dfs_order, "dfs"), ("BFS (черга)", bfs_order, "bfs")):
        root = build()
        result = color_traversal(traversal(root))
        print(f"{name}: " + ", ".join(f"{v}={c}" for v, c in result))
        # підсумкова картинка: усі вузли пофарбовані за порядком обходу
        draw_tree(root, title=f"{name}: від темного (перший) до світлого (останній)",
                  save_path=f"images/{fname}_final.png")
        # покрокова візуалізація
        show_steps(build, traversal, name, save_path=f"images/{fname}_steps.png")

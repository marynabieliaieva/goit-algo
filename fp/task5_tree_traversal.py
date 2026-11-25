"""Task 5. Visualizing binary tree traversal: depth-first (DFS, stack) and breadth-first (BFS, queue).

Every visited node gets a unique #RRGGBB color,
from dark (visited first) to light (visited last).
"""

import heapq
from collections import deque

import matplotlib.pyplot as plt

from task4_heap_visualization import heap_to_tree
from tree_viz import draw_tree

DARK = (0x0B, 0x1E, 0x3F)   # dark blue
LIGHT = (0xBF, 0xE6, 0xFF)  # light blue


def gradient(n):
    """List of n #RRGGBB colors going from dark to light."""
    colors = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        r, g, b = (round(d + (l - d) * t) for d, l in zip(DARK, LIGHT))
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def dfs_order(root):
    """Depth-first (pre-order) traversal using a stack, no recursion."""
    order, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        order.append(node)
        # push the right child first so the left one is popped earlier
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_order(root):
    """Breadth-first traversal using a queue, no recursion."""
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
    """Color the nodes in traversal order and return a list of (value, color)."""
    colors = gradient(len(order))
    for node, color in zip(order, colors):
        node.color = color
    return [(node.val, node.color) for node in order]


def show_steps(build_root, traversal, name):
    """Step by step: at step k the first k visited nodes are colored, the rest are gray."""
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
        draw_tree(root, title=f"{name}: step {k + 1}, node {order[k].val}", ax=axes[k], node_size=900)
    for ax in axes[steps:]:
        ax.axis("off")
    fig.suptitle(f"{name}: order {' -> '.join(str(n.val) for n in order)}", fontsize=14)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = [10, 4, 15, 1, 7, 3, 20, 8, 2]
    heapq.heapify(data)

    def build():
        return heap_to_tree(data)

    for name, traversal in (("DFS (stack)", dfs_order), ("BFS (queue)", bfs_order)):
        root = build()
        result = color_traversal(traversal(root))
        print(f"{name}: " + ", ".join(f"{v}={c}" for v, c in result))
        # final picture: all nodes colored by traversal order
        draw_tree(root, title=f"{name}: from dark (first) to light (last)")
        # step-by-step visualization
        show_steps(build, traversal, name)

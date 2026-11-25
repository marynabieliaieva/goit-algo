"""Завдання 4. Візуалізація бінарної купи (піраміди).

Купа зберігається в масиві: для елемента з індексом i
лівий нащадок має індекс 2*i + 1, правий — 2*i + 2.
Функція heap_to_tree будує з цього масиву дерево вузлів Node і малює його.
"""

import heapq
from pathlib import Path

from tree_viz import Node, draw_tree


def heap_to_tree(heap, index=0):
    """Рекурсивно перетворює масив-купу на дерево з вузлів Node."""
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def draw_heap(heap, title="Бінарна купа", save_path=None):
    if not heap:
        print("Купа порожня — нічого малювати.")
        return
    root = heap_to_tree(heap)
    draw_tree(root, title=title, save_path=save_path)


if __name__ == "__main__":
    data = [10, 4, 15, 1, 7, 3, 20, 8, 2]
    heap = data[:]
    heapq.heapify(heap)  # перетворюємо список на min-купу
    print("Вихідні дані:", data)
    print("Купа (масив):", heap)

    Path("images").mkdir(exist_ok=True)
    draw_heap(heap, title=f"Min-купа: {heap}", save_path="images/heap.png")

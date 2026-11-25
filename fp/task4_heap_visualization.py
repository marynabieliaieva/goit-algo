"""Task 4. Binary heap visualization.

A heap is stored as an array: for the element at index i
the left child is at 2*i + 1 and the right child is at 2*i + 2.
heap_to_tree builds a tree of Node objects from that array, which is then drawn.
"""

import heapq

from tree_viz import Node, draw_tree


def heap_to_tree(heap, index=0):
    """Recursively convert a heap array into a tree of Node objects."""
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def draw_heap(heap, title="Binary heap"):
    if not heap:
        print("The heap is empty, nothing to draw.")
        return
    root = heap_to_tree(heap)
    draw_tree(root, title=title)


if __name__ == "__main__":
    data = [10, 4, 15, 1, 7, 3, 20, 8, 2]
    heap = data[:]
    heapq.heapify(heap)  # turn the list into a min-heap
    print("Input data: ", data)
    print("Heap array: ", heap)
    draw_heap(heap, title=f"Min-heap: {heap}")

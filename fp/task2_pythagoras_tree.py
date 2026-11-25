"""Task 2. The "Pythagoras tree" fractal drawn with recursion.

Usage:  python task2_pythagoras_tree.py        (the recursion level is asked interactively)
        python task2_pythagoras_tree.py 8      (the recursion level as an argument)
"""

import math
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ANGLE = math.radians(45)  # angle between the square's top side and the left branch


def draw_square(ax, x, y, size, angle, level, max_level):
    """Draw a square with bottom-left corner (x, y), side `size`, rotated by `angle`,
    then recursively place two smaller squares on its top side."""
    # Vectors along the base and upwards (perpendicular)
    dx, dy = size * math.cos(angle), size * math.sin(angle)
    ux, uy = -dy, dx

    p0 = (x, y)
    p1 = (x + dx, y + dy)
    p2 = (x + dx + ux, y + dy + uy)
    p3 = (x + ux, y + uy)

    # color: from brown (trunk) to green (leaves)
    t = level / max(max_level, 1)
    color = (0.45 * (1 - t), 0.25 + 0.5 * t, 0.1)
    ax.add_patch(Polygon([p0, p1, p2, p3], closed=True, facecolor=color, edgecolor="black", linewidth=0.3))

    if level >= max_level:
        return

    # Left branch: sits on the top side, rotated by +ANGLE
    left_size = size * math.cos(ANGLE)
    draw_square(ax, p3[0], p3[1], left_size, angle + ANGLE, level + 1, max_level)

    # Right branch: starts at the apex of the triangle above the top side
    right_size = size * math.sin(ANGLE)
    apex_x = p3[0] + left_size * math.cos(angle + ANGLE)
    apex_y = p3[1] + left_size * math.sin(angle + ANGLE)
    draw_square(ax, apex_x, apex_y, right_size, angle + ANGLE - math.pi / 2, level + 1, max_level)


def pythagoras_tree(level):
    fig, ax = plt.subplots(figsize=(9, 7))
    draw_square(ax, -0.5, 0, 1, 0, 0, level)
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    ax.set_title(f"Pythagoras tree, recursion level = {level}")
    plt.show()


def read_level():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = input("Enter the recursion level (0-14, recommended 8): ").strip() or "8"
    try:
        level = int(raw)
    except ValueError:
        sys.exit(f"Error: '{raw}' is not an integer.")
    if not 0 <= level <= 14:
        sys.exit("Error: the recursion level must be between 0 and 14 (higher levels take too long to draw).")
    return level


if __name__ == "__main__":
    pythagoras_tree(read_level())

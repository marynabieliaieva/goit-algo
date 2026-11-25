"""Завдання 2. Фрактал "дерево Піфагора" за допомогою рекурсії.

Запуск:  python task2_pythagoras_tree.py        (рівень рекурсії буде запитано)
         python task2_pythagoras_tree.py 8      (рівень рекурсії як аргумент)
"""

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ANGLE = math.radians(45)  # кут між основою квадрата і лівою гілкою


def draw_square(ax, x, y, size, angle, level, max_level):
    """Малює квадрат з нижньою лівою вершиною (x, y), стороною size, повернутий на angle,
    і рекурсивно ставить на його верхню сторону два менші квадрати."""
    # Вектори вздовж основи і вгору (перпендикуляр)
    dx, dy = size * math.cos(angle), size * math.sin(angle)
    ux, uy = -dy, dx

    p0 = (x, y)
    p1 = (x + dx, y + dy)
    p2 = (x + dx + ux, y + dy + uy)
    p3 = (x + ux, y + uy)

    # колір: від коричневого (стовбур) до зеленого (листя)
    t = level / max(max_level, 1)
    color = (0.45 * (1 - t), 0.25 + 0.5 * t, 0.1)
    ax.add_patch(Polygon([p0, p1, p2, p3], closed=True, facecolor=color, edgecolor="black", linewidth=0.3))

    if level >= max_level:
        return

    # Ліва гілка: стоїть на верхній стороні, повернута на +ANGLE
    left_size = size * math.cos(ANGLE)
    draw_square(ax, p3[0], p3[1], left_size, angle + ANGLE, level + 1, max_level)

    # Права гілка: починається у вершині трикутника над верхньою стороною
    right_size = size * math.sin(ANGLE)
    apex_x = p3[0] + left_size * math.cos(angle + ANGLE)
    apex_y = p3[1] + left_size * math.sin(angle + ANGLE)
    draw_square(ax, apex_x, apex_y, right_size, angle + ANGLE - math.pi / 2, level + 1, max_level)


def pythagoras_tree(level, save_path=None):
    fig, ax = plt.subplots(figsize=(9, 7))
    draw_square(ax, -0.5, 0, 1, 0, 0, level)
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    ax.set_title(f"Дерево Піфагора, рівень рекурсії = {level}")
    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches="tight")
    plt.show()


def read_level():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = input("Введіть рівень рекурсії (0-14, рекомендовано 8): ").strip() or "8"
    try:
        level = int(raw)
    except ValueError:
        sys.exit(f"Помилка: '{raw}' не є цілим числом.")
    if not 0 <= level <= 14:
        sys.exit("Помилка: рівень рекурсії має бути від 0 до 14 (більше — дуже довго малюється).")
    return level


if __name__ == "__main__":
    lvl = read_level()
    Path("images").mkdir(exist_ok=True)
    pythagoras_tree(lvl, save_path=f"images/pythagoras_tree_{lvl}.png")

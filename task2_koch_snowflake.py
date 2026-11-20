"""Завдання 2: фрактал «сніжинка Коха» з рекурсією.

Використання:
    python task2_koch_snowflake.py            # рівень рекурсії запитується у користувача
    python task2_koch_snowflake.py --level 3  # рівень рекурсії через аргумент
"""

import argparse
import turtle


def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    """Рекурсивно малює одну сторону сніжинки (криву Коха)."""
    if order == 0:
        t.forward(size)
        return
    for angle in (60, -120, 60, 0):
        koch_curve(t, order - 1, size / 3)
        t.left(angle)


def draw_koch_snowflake(order: int, size: float = 300) -> None:
    """Малює сніжинку Коха з трьох кривих Коха."""
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Сніжинка Коха, рівень {order}")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    window.mainloop()


def read_level() -> int:
    parser = argparse.ArgumentParser(description="Сніжинка Коха")
    parser.add_argument("--level", type=int, help="Рівень рекурсії (0 і більше)")
    args = parser.parse_args()

    level = args.level
    while level is None or level < 0:
        raw = input("Вкажіть рівень рекурсії (ціле число >= 0): ")
        try:
            level = int(raw)
        except ValueError:
            print("Потрібно ввести ціле число.")
            level = None
            continue
        if level < 0:
            print("Рівень не може бути від'ємним.")
    return level


if __name__ == "__main__":
    draw_koch_snowflake(read_level())

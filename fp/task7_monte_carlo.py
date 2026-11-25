"""Завдання 7. Метод Монте-Карло: імовірності сум при киданні двох кубиків."""

import random
from pathlib import Path

import matplotlib.pyplot as plt

N_THROWS = 1_000_000


def simulate(n, seed=42):
    rng = random.Random(seed)
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(n):
        counts[rng.randint(1, 6) + rng.randint(1, 6)] += 1
    return {s: c / n for s, c in counts.items()}, counts


def analytical():
    """Точні ймовірності: кількість способів отримати суму s з 36 можливих."""
    return {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}


def print_table(mc, exact, counts):
    print(f"{'Сума':>4} | {'Кількість':>9} | {'Монте-Карло':>11} | {'Аналітично':>10} | {'Різниця':>8}")
    print("-" * 56)
    for s in range(2, 13):
        diff = mc[s] - exact[s]
        print(f"{s:>4} | {counts[s]:>9} | {mc[s]:>10.2%} | {exact[s]:>9.2%} | {diff:>+8.3%}")
    max_diff = max(abs(mc[s] - exact[s]) for s in mc)
    print(f"\nМаксимальне відхилення: {max_diff:.3%}")


def plot(mc, exact, n, save_path=None):
    sums = list(range(2, 13))
    width = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([s - width / 2 for s in sums], [mc[s] * 100 for s in sums], width, label=f"Монте-Карло ({n:,} кидків)")
    ax.bar([s + width / 2 for s in sums], [exact[s] * 100 for s in sums], width, label="Аналітично")
    for s in sums:
        ax.text(s - width / 2, mc[s] * 100 + 0.2, f"{mc[s]:.2%}", ha="center", fontsize=7)
    ax.set_xticks(sums)
    ax.set_xlabel("Сума на двох кубиках")
    ax.set_ylabel("Імовірність, %")
    ax.set_title("Імовірності сум при киданні двох кубиків")
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=110)
    plt.show()


if __name__ == "__main__":
    mc, counts = simulate(N_THROWS)
    exact = analytical()
    print_table(mc, exact, counts)

    # як точність залежить від кількості кидків
    print("\nЗбіжність (максимальне відхилення від точних значень):")
    for n in (100, 1_000, 10_000, 100_000, 1_000_000):
        p, _ = simulate(n)
        print(f"  {n:>9,} кидків: {max(abs(p[s] - exact[s]) for s in p):.3%}")

    Path("images").mkdir(exist_ok=True)
    plot(mc, exact, N_THROWS, save_path="images/monte_carlo.png")

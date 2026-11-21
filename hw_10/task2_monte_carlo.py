"""Завдання 2: визначений інтеграл методом Монте-Карло."""

import matplotlib

matplotlib.use("Agg")  # малюємо у файл, вікно не потрібне

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


def f(x):
    return x ** 2


A, B = 0, 2  # межі інтегрування
EXACT = (B ** 3 - A ** 3) / 3  # аналітично: x^3 / 3 від 0 до 2 = 8/3
CHUNK = 100_000  # точки генеруємо порціями, щоб не тримати мільйони в пам'яті


def monte_carlo_hit_or_miss(func, a, b, n, rng):
    """Метод «влучань»: кидаємо n випадкових точок у прямокутник
    [a, b] x [0, max f] і рахуємо частку точок, що лягли під графік.
    Площа під кривою = частка влучань * площа прямокутника.
    """
    y_max = max(func(a), func(b))  # x^2 зростає на [0, 2], максимум у кінці
    hits, done = 0, 0
    while done < n:
        size = min(CHUNK, n - done)
        x = rng.uniform(a, b, size)
        y = rng.uniform(0, y_max, size)
        hits += np.count_nonzero(y <= func(x))
        done += size
    return hits / n * (b - a) * y_max


def monte_carlo_mean(func, a, b, n, rng):
    """Метод середнього значення: інтеграл ≈ (b - a) * середнє f(x)
    у n випадкових точках відрізка [a, b].
    """
    total, done = 0.0, 0
    while done < n:
        size = min(CHUNK, n - done)
        total += func(rng.uniform(a, b, size)).sum()
        done += size
    return (b - a) * total / n


def plot(rng, path="monte_carlo.png", n_points=2000):
    xs = np.linspace(-0.5, 2.5, 400)
    fig, ax = plt.subplots()
    ax.plot(xs, f(xs), "r", linewidth=2)
    ix = np.linspace(A, B)
    ax.fill_between(ix, f(ix), color="gray", alpha=0.3)

    x = rng.uniform(A, B, n_points)
    y = rng.uniform(0, f(B), n_points)
    inside = y <= f(x)
    ax.scatter(x[inside], y[inside], s=2, color="green", label="під кривою")
    ax.scatter(x[~inside], y[~inside], s=2, color="blue", label="над кривою")

    ax.set_xlim([xs[0], xs[-1]])
    ax.set_ylim([0, f(xs).max() + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=A, color="gray", linestyle="--")
    ax.axvline(x=B, color="gray", linestyle="--")
    ax.set_title(f"Монте-Карло для f(x) = x^2 від {A} до {B}")
    ax.legend(loc="upper left")
    ax.grid()
    fig.savefig(path, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    quad_result, quad_error = spi.quad(f, A, B)
    print(f"Аналітично:  {EXACT:.6f}")
    print(f"SciPy quad:  {quad_result:.6f} (оцінка похибки {quad_error:.1e})\n")

    print(f"{'N':>10} | {'Влучання':>9} | {'Похибка':>8} | {'Середнє':>9} | {'Похибка':>8}")
    print("-" * 56)
    for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
        hit = monte_carlo_hit_or_miss(f, A, B, n, rng)
        mean = monte_carlo_mean(f, A, B, n, rng)
        print(f"{n:>10} | {hit:>9.5f} | {abs(hit - EXACT) / EXACT:>7.2%} | "
              f"{mean:>9.5f} | {abs(mean - EXACT) / EXACT:>7.2%}")

    # Розкид результату: 20 незалежних запусків по 100 000 точок
    for name, method in [("влучання", monte_carlo_hit_or_miss), ("середнє", monte_carlo_mean)]:
        runs = [method(f, A, B, 100_000, rng) for _ in range(20)]
        print(f"\n20 запусків по 100 000 точок ({name}): середнє {np.mean(runs):.5f}, "
              f"стандартне відхилення {np.std(runs):.5f}", end="")
    print()

    plot(rng)
    print("\nГрафік збережено у monte_carlo.png")

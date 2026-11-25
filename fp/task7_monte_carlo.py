"""Task 7. Monte Carlo method: probabilities of sums when rolling two dice."""

import random

import matplotlib.pyplot as plt

N_THROWS = 1_000_000


def simulate(n, seed=42):
    rng = random.Random(seed)
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(n):
        counts[rng.randint(1, 6) + rng.randint(1, 6)] += 1
    return {s: c / n for s, c in counts.items()}, counts


def analytical():
    """Exact probabilities: number of ways to get sum s out of 36 outcomes."""
    return {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}


def print_table(mc, exact, counts):
    print(f"{'Sum':>4} | {'Count':>9} | {'Monte Carlo':>11} | {'Analytical':>10} | {'Diff':>8}")
    print("-" * 56)
    for s in range(2, 13):
        diff = mc[s] - exact[s]
        print(f"{s:>4} | {counts[s]:>9} | {mc[s]:>10.2%} | {exact[s]:>9.2%} | {diff:>+8.3%}")
    max_diff = max(abs(mc[s] - exact[s]) for s in mc)
    print(f"\nMax deviation: {max_diff:.3%}")


def plot(mc, exact, n):
    sums = list(range(2, 13))
    width = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([s - width / 2 for s in sums], [mc[s] * 100 for s in sums], width, label=f"Monte Carlo ({n:,} rolls)")
    ax.bar([s + width / 2 for s in sums], [exact[s] * 100 for s in sums], width, label="Analytical")
    for s in sums:
        ax.text(s - width / 2, mc[s] * 100 + 0.2, f"{mc[s]:.2%}", ha="center", fontsize=7)
    ax.set_xticks(sums)
    ax.set_xlabel("Sum of two dice")
    ax.set_ylabel("Probability, %")
    ax.set_title("Probabilities of sums when rolling two dice")
    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    mc, counts = simulate(N_THROWS)
    exact = analytical()
    print_table(mc, exact, counts)

    # how accuracy depends on the number of rolls
    print("\nConvergence (max deviation from exact values):")
    for n in (100, 1_000, 10_000, 100_000, 1_000_000):
        p, _ = simulate(n)
        print(f"  {n:>9,} rolls: {max(abs(p[s] - exact[s]) for s in p):.3%}")
    plot(mc, exact, N_THROWS)

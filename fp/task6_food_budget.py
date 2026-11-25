"""Task 6. Choosing food with maximum total calories within a budget:
a greedy algorithm and dynamic programming (0/1 knapsack)."""

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items, budget):
    """Take dishes in descending order of calories/cost ratio while they fit
    into the budget. Fast, but not always optimal."""
    ranked = sorted(items.items(), key=lambda kv: kv[1]["calories"] / kv[1]["cost"], reverse=True)
    chosen, total_cost, total_calories = [], 0, 0
    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]
    return chosen, total_cost, total_calories


def dynamic_programming(items, budget):
    """Classic 0/1 knapsack: dp[i][b] is the max calories using the first i dishes with budget b.
    Always optimal. Complexity O(n * budget)."""
    names = list(items)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # skip the dish
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)  # take the dish

    # rebuild the chosen set by walking the table backwards
    chosen, b = [], budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]
    chosen.reverse()
    total_cost = sum(items[name]["cost"] for name in chosen)
    return chosen, total_cost, dp[n][budget]


if __name__ == "__main__":
    for budget in (50, 100, 120):
        g = greedy_algorithm(items, budget)
        d = dynamic_programming(items, budget)
        print(f"Budget {budget}:")
        print(f"  Greedy: {g[0]}  cost={g[1]}  calories={g[2]}")
        print(f"  DP:     {d[0]}  cost={d[1]}  calories={d[2]}")
        assert g[1] <= budget and d[1] <= budget
        assert d[2] >= g[2]  # DP is never worse than greedy

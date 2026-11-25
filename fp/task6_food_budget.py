"""Завдання 6. Вибір їжі з максимальною калорійністю в межах бюджету:
жадібний алгоритм і динамічне програмування (задача про рюкзак 0/1)."""

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items, budget):
    """Беремо страви у порядку спадання співвідношення калорії/вартість,
    поки вони вміщуються в бюджет. Швидко, але не завжди оптимально."""
    ranked = sorted(items.items(), key=lambda kv: kv[1]["calories"] / kv[1]["cost"], reverse=True)
    chosen, total_cost, total_calories = [], 0, 0
    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]
    return chosen, total_cost, total_calories


def dynamic_programming(items, budget):
    """Класичний рюкзак 0/1: dp[i][b] — максимум калорій з перших i страв при бюджеті b.
    Завжди дає оптимальний результат. Складність O(n * budget)."""
    names = list(items)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо страву
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)  # беремо страву

    # відновлюємо набір страв, ідучи по таблиці назад
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
        print(f"Бюджет {budget}:")
        print(f"  Жадібний: {g[0]}  вартість={g[1]}  калорії={g[2]}")
        print(f"  ДП:       {d[0]}  вартість={d[1]}  калорії={d[2]}")
        assert g[1] <= budget and d[1] <= budget
        assert d[2] >= g[2]  # ДП ніколи не гірше за жадібний

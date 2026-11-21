"""Завдання 1: видача решти жадібним алгоритмом і динамічним програмуванням."""

import timeit

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount, coins=COINS):
    """Жадібний алгоритм: щоразу беремо найбільший номінал, який ще вміщується.

    Повертає словник {номінал: кількість}. Складність O(k), де k — кількість
    номіналів (на кожен номінал одне ділення з остачею), тобто від суми
    час майже не залежить.
    """
    result = {}
    for coin in sorted(coins, reverse=True):
        count, amount = divmod(amount, coin)
        if count:
            result[coin] = count
    return result


def find_min_coins(amount, coins=COINS):
    """Динамічне програмування: мінімальна кількість монет для суми.

    min_coins[s] — найменша кількість монет для суми s,
    last_coin[s] — монета, якою закінчується оптимальний набір для s.
    Заповнюємо таблицю від 1 до amount, потім відновлюємо відповідь
    за last_coin. Складність O(amount * k) за часом і O(amount) за пам'яттю.
    """
    if amount == 0:
        return {}

    inf = float("inf")
    min_coins = [0] + [inf] * amount
    last_coin = [0] * (amount + 1)

    for s in range(1, amount + 1):
        for coin in coins:
            if coin <= s and min_coins[s - coin] + 1 < min_coins[s]:
                min_coins[s] = min_coins[s - coin] + 1
                last_coin[s] = coin

    if min_coins[amount] == inf:
        raise ValueError(f"Суму {amount} неможливо видати цими монетами")

    result = {}
    s = amount
    while s > 0:
        coin = last_coin[s]
        result[coin] = result.get(coin, 0) + 1
        s -= coin
    return dict(sorted(result.items()))


def total_coins(change):
    return sum(change.values())


def benchmark(amounts, repeats=3):
    print(f"{'Сума':>10} | {'Жадібний, мс':>13} | {'ДП, мс':>12} | {'Монет (ж/ДП)':>12}")
    print("-" * 58)
    for amount in amounts:
        t_greedy = min(timeit.repeat(lambda: find_coins_greedy(amount), number=1, repeat=repeats)) * 1000
        t_dp = min(timeit.repeat(lambda: find_min_coins(amount), number=1, repeat=repeats)) * 1000
        g, d = total_coins(find_coins_greedy(amount)), total_coins(find_min_coins(amount))
        print(f"{amount:>10} | {t_greedy:>13.4f} | {t_dp:>12.2f} | {g:>5} / {d:<5}")


if __name__ == "__main__":
    amount = 113
    print("Жадібний алгоритм для 113:", find_coins_greedy(amount))
    print("Динамічне програмування для 113:", find_min_coins(amount))
    print()

    # Перевірка: для набору [50, 25, 10, 5, 2, 1] жадібний алгоритм
    # дає стільки ж монет, скільки й ДП, для кожної суми до 1000.
    for s in range(1001):
        g, d = find_coins_greedy(s), find_min_coins(s)
        assert sum(c * n for c, n in g.items()) == s
        assert sum(c * n for c, n in d.items()) == s
        assert total_coins(g) == total_coins(d)
    print("Перевірка 0..1000: обидва алгоритми дають правильну суму і однакову кількість монет.\n")

    benchmark([113, 1_000, 10_000, 100_000, 1_000_000])

    # Набір, де жадібний алгоритм помиляється
    other = [4, 3, 1]
    print("\nНабір [4, 3, 1], сума 6:")
    print("  жадібний:", find_coins_greedy(6, other), "->", total_coins(find_coins_greedy(6, other)), "монети")
    print("  ДП:      ", find_min_coins(6, other), "->", total_coins(find_min_coins(6, other)), "монети")

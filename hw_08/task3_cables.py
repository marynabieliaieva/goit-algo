"""Завдання 3: об'єднання кабелів з мінімальними витратами (через купу)."""

import heapq


def min_connection_cost(lengths):
    """Повертає (мінімальні загальні витрати, порядок з'єднань).

    Жадібна ідея: щоразу з'єднуємо два найкоротші кабелі. Довжина кабелю
    входить у витрати стільки разів, скільки з'єднань він пройшов, тому
    короткі кабелі вигідно з'єднувати першими, а довгі — якомога пізніше.
    Мінімальна купа дає два найкоротші кабелі за O(log n), загалом O(n log n).
    """
    heap = list(lengths)
    heapq.heapify(heap)

    total = 0
    steps = []
    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        cost = first + second
        total += cost
        steps.append((first, second, cost))
        heapq.heappush(heap, cost)

    return total, steps


if __name__ == "__main__":
    cables = [4, 3, 2, 6]
    total, steps = min_connection_cost(cables)

    print("Довжини кабелів:", cables)
    for i, (a, b, cost) in enumerate(steps, 1):
        print(f"Крок {i}: {a} + {b} = {cost}")
    print("Мінімальні загальні витрати:", total)

    assert total == 29
    assert min_connection_cost([5])[0] == 0
    assert min_connection_cost([])[0] == 0
    assert min_connection_cost([1, 2, 3, 4, 5])[0] == 33

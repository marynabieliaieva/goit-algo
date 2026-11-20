"""Завдання 3: порівняння сортування злиттям, вставками та Timsort за допомогою timeit."""

import random
import timeit


def insertion_sort(arr: list) -> list:
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def timsort(arr: list) -> list:
    return sorted(arr)


ALGORITHMS = {
    "Вставками": insertion_sort,
    "Злиттям": merge_sort,
    "Timsort (sorted)": timsort,
}

SIZES = [100, 1_000, 5_000, 10_000]


def make_datasets(size: int) -> dict:
    random.seed(42)
    data = [random.randint(0, 100_000) for _ in range(size)]
    nearly = sorted(data)
    for _ in range(max(1, size // 100)):  # ~1% елементів переставлено
        a, b = random.randrange(size), random.randrange(size)
        nearly[a], nearly[b] = nearly[b], nearly[a]
    return {
        "випадковий": data,
        "відсортований": sorted(data),
        "майже відсортований": nearly,
        "зворотний": sorted(data, reverse=True),
    }


def measure(func, data: list) -> float:
    # Повільне сортування вставками на великих даних запускаємо менше разів.
    number = 1 if len(data) >= 5_000 else 5
    return timeit.timeit(lambda: func(data), number=number) / number


def main() -> None:
    # Перевірка коректності перед замірами.
    sample = [random.randint(-50, 50) for _ in range(200)]
    for name, func in ALGORITHMS.items():
        assert func(sample) == sorted(sample), name

    header = f"| {'Набір даних':<20} | {'n':>6} | " + " | ".join(f"{n:>16}" for n in ALGORITHMS) + " |"
    print(header)
    print("|" + "|".join("-" * (len(c)) for c in header.split("|")[1:-1]) + "|")
    for size in SIZES:
        for kind, data in make_datasets(size).items():
            times = [measure(func, data) for func in ALGORITHMS.values()]
            row = " | ".join(f"{t:>14.6f} с" for t in times)
            print(f"| {kind:<20} | {size:>6} | {row} |")


if __name__ == "__main__":
    main()

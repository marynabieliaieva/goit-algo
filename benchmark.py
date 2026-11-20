"""Порівняння швидкості алгоритмів пошуку підрядка на двох статтях (timeit).

Очікує файли article1.txt (стаття 1) і article2.txt (стаття 2) поруч зі скриптом.
"""

import timeit
from pathlib import Path

from substring_search import boyer_moore_search, kmp_search, rabin_karp_search

BASE_DIR = Path(__file__).parent
ARTICLES = {
    "Стаття 1": BASE_DIR / "article1.txt",
    "Стаття 2": BASE_DIR / "article2.txt",
}

# Для кожної статті: підрядок, що є в тексті, і вигаданий підрядок.
PATTERNS = {
    "Стаття 1": {"існуючий": "основне завдання програміста", "вигаданий": "квантовий бульбашковий пошук"},
    "Стаття 2": {"існуючий": "Перевага розгорнутого списку", "вигаданий": "квантовий бульбашковий пошук"},
}

ALGORITHMS = {
    "Боєра-Мура": boyer_moore_search,
    "КМП": kmp_search,
    "Рабіна-Карпа": rabin_karp_search,
}

NUMBER = 20  # кількість повторів для timeit


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Не вдалося прочитати {path}")


def main() -> None:
    totals = {name: 0.0 for name in ALGORITHMS}
    print(f"| {'Текст':<9} | {'Підрядок':<10} | {'Алгоритм':<13} | {'Індекс':>7} | {'Час, мс':>9} |")
    print(f"|{'-' * 11}|{'-' * 12}|{'-' * 15}|{'-' * 9}|{'-' * 11}|")
    for article, path in ARTICLES.items():
        text = read_text(path)
        per_text = {name: 0.0 for name in ALGORITHMS}
        for kind, pattern in PATTERNS[article].items():
            expected = text.find(pattern)
            for name, func in ALGORITHMS.items():
                result = func(text, pattern)
                assert result == expected, f"{name} повернув {result}, очікувалось {expected}"
                seconds = timeit.timeit(lambda: func(text, pattern), number=NUMBER) / NUMBER
                per_text[name] += seconds
                totals[name] += seconds
                print(f"| {article:<9} | {kind:<10} | {name:<13} | {result:>7} | {seconds * 1000:>9.3f} |")
        fastest = min(per_text, key=per_text.get)
        print(f"\nНайшвидший для «{article}» ({len(text)} символів): {fastest}\n")
    fastest_total = min(totals, key=totals.get)
    print("Сумарний час по обох текстах:")
    for name, seconds in sorted(totals.items(), key=lambda item: item[1]):
        print(f"  {name}: {seconds * 1000:.3f} мс")
    print(f"Найшвидший у цілому: {fastest_total}")


if __name__ == "__main__":
    main()

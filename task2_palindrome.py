"""Завдання 2: перевірка паліндрому за допомогою двосторонньої черги (collections.deque).

Перевірка нечутлива до регістру та пробілів і працює для рядків
як з парною, так і з непарною кількістю символів.
"""

from collections import deque


def is_palindrome(text: str) -> bool:
    # Додаємо всі символи (без пробілів, у нижньому регістрі) до двосторонньої черги.
    chars = deque(ch for ch in text.lower() if not ch.isspace())

    # Порівнюємо символи з обох кінців. Якщо символів непарна кількість,
    # середній залишається один у черзі й не потребує порівняння.
    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False
    return True


if __name__ == "__main__":
    examples = [
        "Аргентина манит негра",  # непарна кількість літер без пробілів
        "А роза упала на лапу Азора",
        "Never odd or even",
        "abba",                   # парна кількість
        "racecar",                # непарна кількість
        "Python",
        "",
    ]
    for example in examples:
        print(f"{example!r}: {'паліндром' if is_palindrome(example) else 'не паліндром'}")

    user_text = input("\nВведіть рядок для перевірки: ")
    print("Це паліндром." if is_palindrome(user_text) else "Це не паліндром.")

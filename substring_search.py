"""Алгоритми пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа.

Кожна функція повертає індекс першого входження підрядка в текст або -1.
"""


def build_shift_table(pattern: str) -> dict:
    """Таблиця зсувів (евристика «поганого символу») для Боєра-Мура."""
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


def compute_lps(pattern: str) -> list:
    """Масив найдовших префіксів, що є суфіксами (LPS), для КМП."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def polynomial_hash(s: str, base: int = 256, modulus: int = 101) -> int:
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + ord(char)) % modulus
    return hash_value


def rabin_karp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    m, n = len(pattern), len(text)
    if m > n:
        return -1
    base, modulus = 256, 101
    pattern_hash = polynomial_hash(pattern, base, modulus)
    window_hash = polynomial_hash(text[:m], base, modulus)
    h_multiplier = pow(base, m - 1, modulus)

    for i in range(n - m + 1):
        if pattern_hash == window_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h_multiplier) % modulus
            window_hash = (window_hash * base + ord(text[i + m])) % modulus
    return -1

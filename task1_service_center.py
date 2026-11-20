"""Завдання 1: імітація сервісного центру з чергою заявок (queue.Queue).

Програма в циклі автоматично генерує нові заявки, додає їх до черги
та послідовно обробляє, видаляючи з черги.

Використання:
    python task1_service_center.py              # працює, доки не натиснути Ctrl+C
    python task1_service_center.py --cycles 10  # виконати 10 циклів і завершити
"""

import argparse
import random
import time
from itertools import count
from queue import Queue

# Створити чергу заявок
queue = Queue()

_request_ids = count(1)


def generate_request() -> None:
    """Створює нову заявку з унікальним номером і додає її до черги."""
    request = {
        "id": next(_request_ids),
        "client": random.choice(["Олена", "Андрій", "Марина", "Сергій", "Ірина"]),
        "problem": random.choice(["не вмикається", "розбитий екран", "не заряджається", "повільно працює"]),
    }
    queue.put(request)
    print(f"[+] Нова заявка #{request['id']}: {request['client']} — {request['problem']} "
          f"(у черзі: {queue.qsize()})")


def process_request() -> None:
    """Видаляє заявку з черги та обробляє її, якщо черга не пуста."""
    if not queue.empty():
        request = queue.get()
        print(f"[✓] Оброблено заявку #{request['id']} ({request['client']}) "
              f"(залишилось у черзі: {queue.qsize()})")
        queue.task_done()
    else:
        print("[i] Черга пуста, нових заявок немає.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Імітація обробки заявок у сервісному центрі")
    parser.add_argument("--cycles", type=int, default=None,
                        help="Кількість циклів (за замовчуванням — нескінченно, вихід Ctrl+C)")
    parser.add_argument("--delay", type=float, default=1.0, help="Пауза між циклами, секунди")
    args = parser.parse_args()

    print("Сервісний центр працює. Натисніть Ctrl+C для виходу.\n")
    cycle = 0
    try:
        # Головний цикл програми: поки користувач не вийде з програми
        while args.cycles is None or cycle < args.cycles:
            cycle += 1
            # Іноді надходить кілька заявок, іноді жодної — так черга то росте, то спорожнюється.
            for _ in range(random.randint(0, 2)):
                generate_request()
            process_request()
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\nРоботу завершено користувачем.")
    print(f"Заявок, що залишились у черзі: {queue.qsize()}")


if __name__ == "__main__":
    main()

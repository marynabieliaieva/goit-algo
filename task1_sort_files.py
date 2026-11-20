"""Завдання 1: рекурсивне копіювання файлів із сортуванням за розширенням.

Використання:
    python task1_sort_files.py <вихідна_директорія> [директорія_призначення]

Якщо директорію призначення не вказано, використовується "dist".
"""

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та сортує їх у піддиректорії за розширенням."
    )
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)",
    )
    return parser.parse_args()


def get_extension_folder(file_path: Path) -> str:
    """Назва піддиректорії за розширенням файлу (без крапки, у нижньому регістрі)."""
    ext = file_path.suffix.lower().lstrip(".")
    return ext if ext else "no_extension"


def copy_file(file_path: Path, destination: Path) -> None:
    """Копіює файл у піддиректорію destination/<розширення>."""
    target_dir = destination / get_extension_folder(file_path)
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / file_path.name
        # Якщо файл з такою назвою вже є — додаємо номер, щоб не перезаписати.
        counter = 1
        while target.exists():
            target = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1
        shutil.copy2(file_path, target)
        print(f"Скопійовано: {file_path} -> {target}")
    except (PermissionError, OSError) as error:
        print(f"Не вдалося скопіювати {file_path}: {error}", file=sys.stderr)


def process_directory(directory: Path, destination: Path) -> None:
    """Рекурсивно обходить директорію та копіює всі файли."""
    try:
        items = list(directory.iterdir())
    except (PermissionError, OSError) as error:
        print(f"Немає доступу до {directory}: {error}", file=sys.stderr)
        return

    for item in items:
        # Не заходимо в директорію призначення, якщо вона всередині вихідної.
        if item.resolve() == destination.resolve():
            continue
        if item.is_dir():
            process_directory(item, destination)  # рекурсивний виклик
        elif item.is_file():
            copy_file(item, destination)


def main() -> None:
    args = parse_args()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists() or not source.is_dir():
        print(f"Вихідна директорія не існує або не є директорією: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as error:
        print(f"Не вдалося створити директорію призначення {destination}: {error}", file=sys.stderr)
        sys.exit(1)

    process_directory(source, destination)
    print(f"\nГотово. Файли розсортовано в: {destination.resolve()}")


if __name__ == "__main__":
    main()

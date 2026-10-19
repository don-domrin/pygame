"""Таблица рекордов Золотой лихорадки."""
import json
import os
from datetime import datetime
import settings as s

RECORDS_FILE = "records.json"


def load_records(path: str = RECORDS_FILE) -> list[dict]:
    """Читает таблицу или начинает пустую при ошибке файла."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"Файл {path} повреждён, начинаем таблицу заново.")
        return []
    except OSError as error:
        print(f"Не удалось прочитать {path}: {error}")
        return []
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


def save_records(records: list[dict], path: str = RECORDS_FILE) -> None:
    """Сохраняет таблицу в UTF-8."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {path}: {error}")


def save_match(winner: str, score: str, best: int, path: str = RECORDS_FILE) -> None:
    """Добавляет итог матча."""
    records = load_records(path)
    records.append({"winner": winner, "score": score, "best": best,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M")})
    save_records(records, path)


def print_table(path: str = RECORDS_FILE) -> None:
    """Печатает лучшие результаты."""
    print("\n--- Таблица рекордов ---")
    records = sorted(load_records(path), key=lambda record: record.get("best", 0), reverse=True)
    for number, record in enumerate(records[:s.TABLE_SIZE], start=1):
        print(f'{number}. {record.get("winner", "?")}  '
              f'{record.get("score", "?")}  '
              f'{record.get("best", 0)}  {record.get("date", "?")}')

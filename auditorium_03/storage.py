"""Таблица матчей Арены."""
import json
import os

RECORDS_FILE = "records.json"


def load_records(path: str = RECORDS_FILE) -> list[dict]:
    """Читает записи, не прерывая игру при ошибке файла."""
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
    return data


def save_match(winner: str, score: str, turns: int, path: str = RECORDS_FILE) -> None:
    """Добавляет матч в таблицу."""
    records = load_records(path)
    records.append({"winner": winner, "score": score, "turns": turns})
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {path}: {error}")


def print_table(path: str = RECORDS_FILE) -> None:
    """Печатает десять последних матчей."""
    print("\n--- Таблица матчей ---")
    for number, record in enumerate(load_records(path)[-10:], start=1):
        print(f'{number:>2}. {record["winner"]:<10} {record["score"]:<6} ходов: {record["turns"]}')

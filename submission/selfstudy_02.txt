"""Золотая лихорадка v0.2: шахта."""
import random

MAP_ROWS = [
    "#################",
    "#...............#",
    "#.###...#...###.#",
    "#.#...........#.#",
    "#.#.###.#####.#.#",
    "#...#.......#...#",
    "#.###.#####.###.#",
    "#...............#",
    "#.###.#####.###.#",
    "#...............#",
    "#################",
]
COINS_AT_START = 10
GOLD_AT_START = 3
COIN_VALUE = 1
GOLD_VALUE = 3
MOVES_LIMIT = 40
DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


def create_field() -> list[list[str]]:
    """Создаёт карту из строк."""
    return [list(row) for row in MAP_ROWS]


def create_player() -> dict:
    """Создаёт старателя на начальной клетке."""
    return {"x": 1, "y": 1, "score": 0, "coins": 0, "moves": MOVES_LIMIT}


def is_wall(field: list[list[str]], x: int, y: int) -> bool:
    """Проверяет границы и породу."""
    if y < 0 or y >= len(field) or x < 0 or x >= len(field[0]):
        return True
    return field[y][x] == "#"


def free_cells(field: list[list[str]]) -> list[tuple[int, int]]:
    """Возвращает координаты свободных клеток."""
    cells = []
    for y in range(len(field)):
        for x in range(len(field[0])):
            if not is_wall(field, x, y):
                cells.append((x, y))
    return cells


def create_coins(field: list[list[str]], player: dict) -> list[dict]:
    """Раскладывает десять монет по разным клеткам."""
    cells = free_cells(field)
    cells.remove((player["x"], player["y"]))
    random.shuffle(cells)
    coins = []
    for number in range(min(COINS_AT_START, len(cells))):
        x, y = cells[number]
        gold = number < GOLD_AT_START
        coins.append({"x": x, "y": y, "gold": gold,
                      "value": GOLD_VALUE if gold else COIN_VALUE,
                      "symbol": "G" if gold else "o"})
    return coins


def draw(field: list[list[str]], player: dict, coins: list[dict]) -> None:
    """Печатает копию поля и строку состояния."""
    picture = [row[:] for row in field]
    for coin in coins:
        picture[coin["y"]][coin["x"]] = coin["symbol"]
    picture[player["y"]][player["x"]] = "@"
    print()
    for number, row in enumerate(picture):
        print(f"{number:>2} " + " ".join(row))
    print(f'Очки: {player["score"]}  собрано: {player["coins"]}  '
          f'осталось монет: {len(coins)}  осталось ходов: {player["moves"]}')


def move(player: dict, key: str, field: list[list[str]]) -> str:
    """Делает шаг и тратит ход только при успешном движении."""
    dx, dy = DIRECTIONS[key]
    new_x = player["x"] + dx
    new_y = player["y"] + dy
    if is_wall(field, new_x, new_y):
        return "Впереди порода — шаг не сделан (ход не потрачен)."
    player["x"], player["y"] = new_x, new_y
    player["moves"] -= 1
    return "Шаг сделан."


def collect(player: dict, coins: list[dict]) -> str:
    """Подбирает монету под ногами."""
    for coin in coins:
        if (coin["x"], coin["y"]) == (player["x"], player["y"]):
            coins.remove(coin)
            player["score"] += coin["value"]
            player["coins"] += 1
            if coin["gold"]:
                return f'Золотая монета! +{GOLD_VALUE} очка!'
            return f'Монета! +{COIN_VALUE} очко.'
    return ""


def report(player: dict, coins: list[dict]) -> None:
    """Печатает итог забега и оставшиеся монеты."""
    print(f'\nСобрано монет: {player["coins"]}, очки: {player["score"]}.')
    print(f"Осталось в шахте: {len(coins)}")
    for number, coin in enumerate(coins, start=1):
        kind = "золотая" if coin["gold"] else "обычная"
        print(f'{number}. {kind} монета: ({coin["x"]}, {coin["y"]})')
    print("Шахта пуста!" if not coins else "Хороший улов!" if player["coins"] else "Монеты ещё ждут старателя.")


def main() -> None:
    """Запускает забег до конца ходов, монет или команды выхода."""
    field = create_field()
    player = create_player()
    coins = create_coins(field, player)
    while player["moves"] > 0 and coins:
        draw(field, player, coins)
        command = input("Шаг (w/a/s/d, q — выход): ").strip().lower()
        if command == "q":
            break
        if command not in DIRECTIONS:
            print("Неизвестная команда.")
            continue
        print(move(player, command, field))
        message = collect(player, coins)
        if message:
            print(message)
    draw(field, player, coins)
    report(player, coins)


if __name__ == "__main__":
    main()

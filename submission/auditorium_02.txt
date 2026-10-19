"""Арена v0.2: бой на поле."""

MAP_ROWS = [
    "###############",
    "#.......#.....#",
    "#.#####.#.###.#",
    "#.#...........#",
    "#.#.###.#####.#",
    "#...#.......#.#",
    "#.###.#####.#.#",
    "#.............#",
    "###############",
]
DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
SHOT_DAMAGE = 5
START_HP = 20


def create_field() -> list[list[str]]:
    """Создаёт изменяемую копию карты."""
    return [list(row) for row in MAP_ROWS]


def create_player(name: str, symbol: str, x: int, y: int) -> dict:
    """Создаёт бойца."""
    return {"name": name, "symbol": symbol, "x": x, "y": y,
            "dir": (1, 0), "hp": START_HP}


def is_wall(field: list[list[str]], x: int, y: int) -> bool:
    """Проверяет стену и границы поля."""
    if y < 0 or y >= len(field) or x < 0 or x >= len(field[0]):
        return True
    return field[y][x] == "#"


def draw(field: list[list[str]], players: list[dict], trace: tuple | list = ()) -> None:
    """Печатает карту с трассой и бойцами."""
    picture = [row[:] for row in field]
    for x, y in trace:
        picture[y][x] = "*"
    for player in players:
        picture[player["y"]][player["x"]] = player["symbol"]
    print()
    for row in picture:
        print(" ".join(row))
    for player in players:
        arrow = {(0, -1): "^", (0, 1): "v", (-1, 0): "<", (1, 0): ">"}[player["dir"]]
        print(f'{player["symbol"]} {player["name"]:<8} HP: {player["hp"]:>3}  смотрит: {arrow}')


def move(player: dict, key: str, field: list[list[str]], others: list[dict]) -> str:
    """Поворачивает бойца и двигает, если клетка свободна."""
    dx, dy = DIRECTIONS[key]
    player["dir"] = (dx, dy)
    new_x = player["x"] + dx
    new_y = player["y"] + dy
    if is_wall(field, new_x, new_y):
        return "Впереди стена — шаг не сделан (но поворот засчитан)."
    for other in others:
        if (other["x"], other["y"]) == (new_x, new_y):
            return "Там стоит соперник — не пройти."
    player["x"], player["y"] = new_x, new_y
    return "Шаг сделан."


def shoot(shooter: dict, targets: list[dict], field: list[list[str]]) -> tuple[str, list]:
    """Стреляет по прямой до первой стены или бойца."""
    dx, dy = shooter["dir"]
    x, y = shooter["x"], shooter["y"]
    trace = []
    while True:
        x += dx
        y += dy
        if is_wall(field, x, y):
            return "Пуля ушла в стену.", trace
        trace.append((x, y))
        for target in targets:
            if (target["x"], target["y"]) == (x, y):
                target["hp"] -= SHOT_DAMAGE
                return f'Попадание в {target["name"]}: -{SHOT_DAMAGE} HP!', trace


def main() -> None:
    """Проводит бой двух игроков."""
    field = create_field()
    players = [create_player("Синий", "A", 1, 1),
               create_player("Красный", "B", 13, 7)]
    turn = 0
    trace = []
    while all(player["hp"] > 0 for player in players):
        current = players[turn % 2]
        others = [player for player in players if player is not current]
        draw(field, players, trace)
        trace = []
        command = input(f'\nХод игрока {current["name"]} ({current["symbol"]}): ').strip().lower()
        if command == "q":
            print("Матч прерван.")
            return
        elif command in DIRECTIONS:
            print(" ", move(current, command, field, others))
        elif command == "f":
            message, trace = shoot(current, others, field)
            print(" ", message)
        else:
            print("Неизвестная команда. Ход пропущен.")
        turn += 1
    draw(field, players, trace)
    winner = max(players, key=lambda player: player["hp"])
    print(f'Победил {winner["name"]}! Осталось HP: {winner["hp"]}.')


if __name__ == "__main__":
    main()

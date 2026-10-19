"""Консольная оболочка Золотой лихорадки."""
import settings as s
from game import Game
import storage

TURN_DT = s.CELL / s.PLAYER_SPEED
KEYS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
SYMBOLS = ["A", "B"]


def draw(state: dict) -> None:
    """Печатает поле по снимку ядра."""
    picture = [list(row) for row in s.MAP_ROWS]
    for coin in state["coins"]:
        x = int(coin["x"] // s.CELL)
        y = int(coin["y"] // s.CELL)
        picture[y][x] = "G" if coin["gold"] else "o"
    for player in state["players"]:
        x = int(player["x"] // s.CELL)
        y = int(player["y"] // s.CELL)
        picture[y][x] = SYMBOLS[player["id"]]
    print()
    for row in picture:
        print(" ".join(row))
    print(f'Время: {state["time_left"]:.1f} с')
    for player in state["players"]:
        print(f'{player["name"]}: {player["score"]} очков, монет: {player["coins"]}')


def parse_command(command: str) -> tuple[str, int]:
    """Разбирает движение и число повторений."""
    command = command.strip().lower()
    if not command:
        return "", 1
    if command[0] in KEYS:
        key = command[0]
        count_text = command[1:]
    else:
        key = ""
        count_text = command
    if count_text and not count_text.isdigit():
        return "?", 0
    try:
        count = int(count_text) if count_text else 1
    except ValueError:
        return "?", 0
    return key, count


def main() -> None:
    """Играет матч и записывает результат."""
    game = Game()
    turns = 0
    while not game.over:
        draw(game.state())
        current = game.players[turns % 2]
        command = input(f"Ход {current.name} (w/a/s/d, d4, 8, q): ").strip().lower()
        if command == "q":
            print("Матч прерван.")
            return
        key, repeat = parse_command(command)
        if key == "?" or repeat <= 0:
            print("Введите направление и число повторов либо число ожидания.")
            continue
        for _ in range(repeat):
            if game.over:
                break
            dx, dy = KEYS.get(key, (0, 0))
            game.apply_input(current.pid, {"dx": dx, "dy": dy})
            game.update(TURN_DT)
            game.apply_input(current.pid, {})
        turns += 1
    draw(game.state())
    score = f"{game.players[0].score}:{game.players[1].score}"
    winner = "Ничья" if game.winner_id is None else game.players[game.winner_id].name
    print(f"Матч окончен. {winner}. Счёт {score}.")
    storage.save_match(winner, score, max(player.score for player in game.players))
    storage.print_table()


if __name__ == "__main__":
    main()

"""Консольная оболочка Арены."""
import settings as s
from game import Game
import storage

TURN_DT = s.CELL / s.PLAYER_SPEED
KEYS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
SYMBOLS = ["A", "B"]


def draw(state: dict) -> None:
    """Рисует полученный от ядра снимок."""
    picture = [list(row) for row in s.MAP_ROWS]
    for bullet in state["bullets"]:
        x = int(bullet["x"] // s.CELL)
        y = int(bullet["y"] // s.CELL)
        if 0 <= x < s.MAP_W and 0 <= y < s.MAP_H:
            picture[y][x] = "*"
    for player in state["players"]:
        if player["alive"]:
            x = int(player["x"] // s.CELL)
            y = int(player["y"] // s.CELL)
            picture[y][x] = SYMBOLS[player["id"]]
    print()
    for row in picture:
        print(" ".join(row))
    for player in state["players"]:
        symbol = SYMBOLS[player["id"]]
        print(f'{symbol} {player["name"]:<8} HP {player["hp"]:>3}  очки: {player["score"]}')


def main() -> None:
    """Запускает матч на одной клавиатуре."""
    game = Game()
    turns = 0
    while not game.over:
        draw(game.state())
        current = game.players[turns % 2]
        if not current.alive:
            waiting = max(1, round(current.respawn_timer / TURN_DT))
            print(f"\n{current.name} погиб и возрождается. Осталось ходов: {waiting}")
            game.update(TURN_DT)
            turns += 1
            continue
        command = input(f"\nХод: {current.name} > ").strip().lower()
        if command == "q":
            print("Матч прерван.")
            return
        if command in KEYS:
            dx, dy = KEYS[command]
            game.apply_input(current.pid, {"dx": dx, "dy": dy})
        elif command == "f":
            game.apply_input(current.pid, {"shoot": True})
        game.update(TURN_DT)
        game.apply_input(current.pid, {})
        turns += 1
    draw(game.state())
    winner = game.players[game.winner_id]
    score = f"{game.players[0].score}:{game.players[1].score}"
    print(f"Победил {winner.name}! Счёт {score}, ходов: {turns}")
    storage.save_match(winner.name, score, turns)
    storage.print_table()


if __name__ == "__main__":
    main()

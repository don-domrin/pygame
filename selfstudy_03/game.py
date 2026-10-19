"""Игровое ядро Золотой лихорадки."""
import random
import settings as s
from entities import Coin, Player


class Game:
    """Правила и состояние шахты."""

    def __init__(self, player_names: list[str] | None = None):
        names = player_names or s.NAMES
        self.field = [list(row) for row in s.MAP_ROWS]
        self.free_cells = self._collect_free_cells()
        self.players = [Player(i, names[i]) for i in range(len(s.SPAWNS))]
        self.coins: list[Coin] = []
        self.time_left = s.MATCH_TIME
        self.spawn_timer = s.SPAWN_INTERVAL
        self.over = False
        self.winner_id: int | None = None
        for _ in range(s.COINS_ON_FIELD):
            self.spawn_coin()

    def _collect_free_cells(self) -> list[tuple[int, int]]:
        """Находит клетки без породы."""
        cells = []
        for y in range(s.MAP_H):
            for x in range(s.MAP_W):
                if not self.is_wall(x, y):
                    cells.append((x, y))
        return cells

    def is_wall(self, cell_x: int, cell_y: int) -> bool:
        """Проверяет породу и границу карты."""
        if not (0 <= cell_x < s.MAP_W and 0 <= cell_y < s.MAP_H):
            return True
        return self.field[cell_y][cell_x] == "#"

    def hits_wall(self, x: float, y: float, radius: float) -> bool:
        """Проверяет четыре угла вокруг объекта."""
        for corner_x in (x - radius, x + radius):
            for corner_y in (y - radius, y + radius):
                if self.is_wall(int(corner_x // s.CELL), int(corner_y // s.CELL)):
                    return True
        return False

    def spawn_coin(self) -> None:
        """Кладёт монету в случайную незанятую клетку."""
        busy = {coin.cell for coin in self.coins if coin.alive}
        busy.update(player.cell for player in self.players)
        available = [cell for cell in self.free_cells if cell not in busy]
        if not available:
            return
        cell_x, cell_y = random.choice(available)
        self.coins.append(Coin(cell_x, cell_y, gold=random.random() < s.GOLD_CHANCE))

    def apply_input(self, pid: int, data: dict) -> None:
        """Принимает движение игрока."""
        player = self.players[pid]
        player.input = {"dx": float(data.get("dx", 0.0)),
                        "dy": float(data.get("dy", 0.0))}

    def update(self, dt: float) -> None:
        """Продвигает шахту на dt секунд."""
        if self.over:
            return
        self.time_left = max(0.0, self.time_left - dt)
        for player in self.players:
            self._update_player(player, dt)
        for coin in self.coins:
            coin.update(dt)
        self._collect_coins()
        self.coins = [coin for coin in self.coins if coin.alive]
        self._spawn_tick(dt)
        if self.time_left <= 0:
            self._finish()

    def _update_player(self, player: Player, dt: float) -> None:
        """Двигает старателя со скольжением вдоль стен."""
        player.boost = max(0.0, player.boost - dt)
        dx, dy = player.input["dx"], player.input["dy"]
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return
        dx, dy = dx / length, dy / length
        player.dir_x, player.dir_y = dx, dy
        step = player.speed * dt
        if not self.hits_wall(player.x + dx * step, player.y, player.radius):
            player.x += dx * step
        if not self.hits_wall(player.x, player.y + dy * step, player.radius):
            player.y += dy * step

    def _collect_coins(self) -> None:
        """Отдаёт каждую монету только одному игроку."""
        for coin in self.coins:
            if not coin.alive:
                continue
            for player in self.players:
                if player.overlaps(coin):
                    coin.alive = False
                    player.take_coin(coin.value)
                    break

    def _spawn_tick(self, dt: float) -> None:
        """Появляет монеты по таймеру."""
        self.spawn_timer -= dt
        while self.spawn_timer <= 0:
            self.spawn_timer += s.SPAWN_INTERVAL
            if len(self.coins) < s.COINS_ON_FIELD:
                self.spawn_coin()

    def _finish(self) -> None:
        """Определяет победителя по очкам."""
        self.over = True
        best = max(player.score for player in self.players)
        leaders = [player for player in self.players if player.score == best]
        self.winner_id = leaders[0].pid if len(leaders) == 1 else None

    def state(self) -> dict:
        """Снимок шахты для консоли или сети."""
        return {"time_left": round(self.time_left, 2),
                "players": [player.to_dict() for player in self.players],
                "coins": [coin.to_dict() for coin in self.coins],
                "over": self.over, "winner": self.winner_id}

"""Игровое ядро Арены."""
import settings as s
from entities import Bullet, Player


class Game:
    """Правила и состояние матча."""

    def __init__(self, player_names: list[str] | None = None):
        names = player_names or s.NAMES
        self.field = [list(row) for row in s.MAP_ROWS]
        self.players = [Player(i, names[i]) for i in range(len(s.SPAWNS))]
        self.bullets: list[Bullet] = []
        self.time = 0.0
        self.over = False
        self.winner_id: int | None = None

    def is_wall(self, cell_x: int, cell_y: int) -> bool:
        """Проверяет клетку карты."""
        if not (0 <= cell_y < s.MAP_H and 0 <= cell_x < s.MAP_W):
            return True
        return self.field[cell_y][cell_x] == "#"

    def hits_wall(self, x: float, y: float, radius: float) -> bool:
        """Проверяет четыре угла квадрата вокруг объекта."""
        for corner_x in (x - radius, x + radius):
            for corner_y in (y - radius, y + radius):
                if self.is_wall(int(corner_x // s.CELL), int(corner_y // s.CELL)):
                    return True
        return False

    def apply_input(self, pid: int, data: dict) -> None:
        """Принимает направление движения и выстрел."""
        player = self.players[pid]
        player.input = {"dx": float(data.get("dx", 0.0)),
                        "dy": float(data.get("dy", 0.0)),
                        "shoot": bool(data.get("shoot", False))}

    def update(self, dt: float) -> None:
        """Продвигает мир на dt секунд."""
        if self.over:
            return
        self.time += dt
        for player in self.players:
            self._update_player(player, dt)
        for bullet in list(self.bullets):
            self._update_bullet(bullet, dt)
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]

    def _update_player(self, player: Player, dt: float) -> None:
        """Двигает бойца и выпускает пулю."""
        if not player.alive:
            player.respawn_timer -= dt
            if player.respawn_timer <= 0:
                player.respawn()
            return
        player.cooldown = max(0.0, player.cooldown - dt)
        dx, dy = player.input["dx"], player.input["dy"]
        length = (dx * dx + dy * dy) ** 0.5
        if length > 0:
            dx, dy = dx / length, dy / length
            player.dir_x, player.dir_y = dx, dy
            step = s.PLAYER_SPEED * dt
            if not self.hits_wall(player.x + dx * step, player.y, player.radius):
                player.x += dx * step
            if not self.hits_wall(player.x, player.y + dy * step, player.radius):
                player.y += dy * step
        if player.input["shoot"] and player.cooldown == 0:
            self.bullets.append(Bullet(player.x, player.y,
                                       player.dir_x, player.dir_y, player.pid))
            player.cooldown = s.SHOOT_COOLDOWN

    def _update_bullet(self, bullet: Bullet, dt: float) -> None:
        """Двигает пулю небольшими шагами до столкновения."""
        steps = max(1, int((abs(bullet.vx) + abs(bullet.vy)) * dt / 8) + 1)
        for _ in range(steps):
            bullet.x += bullet.vx * dt / steps
            bullet.y += bullet.vy * dt / steps
            if self.hits_wall(bullet.x, bullet.y, bullet.radius):
                bullet.alive = False
                return
            for player in self.players:
                if player.alive and player.pid != bullet.owner_id and player.overlaps(bullet):
                    bullet.alive = False
                    if player.take_damage(s.BULLET_DAMAGE):
                        self._score_point(bullet.owner_id)
                    return

    def _score_point(self, pid: int) -> None:
        """Начисляет очко за гибель соперника."""
        player = self.players[pid]
        player.score += 1
        if player.score >= s.WIN_SCORE:
            self.over = True
            self.winner_id = pid

    def state(self) -> dict:
        """Снимок мира для консоли или сети."""
        return {"t": round(self.time, 2),
                "players": [player.to_dict() for player in self.players],
                "bullets": [bullet.to_dict() for bullet in self.bullets],
                "over": self.over, "winner": self.winner_id}

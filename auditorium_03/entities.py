"""Бойцы и пули Арены."""
import settings as s


class Entity:
    """Объект с координатами и радиусом."""

    def __init__(self, x: float, y: float, radius: float):
        self.x = float(x)
        self.y = float(y)
        self.radius = float(radius)
        self.alive = True

    @property
    def cell(self) -> tuple[int, int]:
        """Клетка объекта на поле."""
        return int(self.x // s.CELL), int(self.y // s.CELL)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x:g}, y={self.y:g})"

    def distance_to(self, other: "Entity") -> float:
        """Расстояние между центрами."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def overlaps(self, other: "Entity") -> bool:
        """Проверяет пересечение объектов."""
        return self.distance_to(other) < self.radius + other.radius


class Player(Entity):
    """Боец Арены."""

    def __init__(self, pid: int, name: str):
        cell_x, cell_y = s.SPAWNS[pid]
        super().__init__(cell_x * s.CELL + s.CELL / 2,
                         cell_y * s.CELL + s.CELL / 2, s.PLAYER_RADIUS)
        self.pid = pid
        self.name = name
        self.hp = s.PLAYER_HP
        self.score = 0
        self.dir_x, self.dir_y = 1.0, 0.0
        self.cooldown = 0.0
        self.respawn_timer = 0.0
        self.input = {"dx": 0.0, "dy": 0.0, "shoot": False}

    def respawn(self) -> None:
        """Возвращает бойца на старт."""
        cell_x, cell_y = s.SPAWNS[self.pid]
        self.x = cell_x * s.CELL + s.CELL / 2
        self.y = cell_y * s.CELL + s.CELL / 2
        self.hp = s.PLAYER_HP
        self.alive = True
        self.cooldown = 0.0
        self.respawn_timer = 0.0

    def take_damage(self, amount: int) -> bool:
        """Отнимает HP и сообщает, погиб ли боец."""
        if not self.alive:
            return False
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False
            self.respawn_timer = s.RESPAWN_TIME
            return True
        return False

    def to_dict(self) -> dict:
        """Снимок бойца для клиента."""
        return {"id": self.pid, "name": self.name,
                "x": round(self.x, 1), "y": round(self.y, 1),
                "dx": self.dir_x, "dy": self.dir_y,
                "hp": self.hp, "score": self.score, "alive": self.alive}


class Bullet(Entity):
    """Пуля, летящая по прямой."""

    def __init__(self, x: float, y: float, dir_x: float, dir_y: float, owner_id: int):
        super().__init__(x, y, s.BULLET_RADIUS)
        self.vx = dir_x * s.BULLET_SPEED
        self.vy = dir_y * s.BULLET_SPEED
        self.owner_id = owner_id

    def to_dict(self) -> dict:
        """Координаты пули для клиента."""
        return {"x": round(self.x, 1), "y": round(self.y, 1)}

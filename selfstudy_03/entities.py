"""Старатели и монеты."""
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
        """Клетка объекта."""
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
    """Старатель, собирающий монеты."""

    def __init__(self, pid: int, name: str):
        cell_x, cell_y = s.SPAWNS[pid]
        super().__init__(cell_x * s.CELL + s.CELL / 2,
                         cell_y * s.CELL + s.CELL / 2, s.PLAYER_RADIUS)
        self.pid = pid
        self.name = name
        self.score = 0
        self.coins = 0
        self.boost = 0.0
        self.dir_x, self.dir_y = 1.0, 0.0
        self.input = {"dx": 0.0, "dy": 0.0}

    @property
    def speed(self) -> float:
        """Текущая скорость с учётом ускорения."""
        return s.BOOST_SPEED if self.boost > 0 else s.PLAYER_SPEED

    def take_coin(self, value: int) -> None:
        """Добавляет очки и ускоряет старателя."""
        self.score += value
        self.coins += 1
        self.boost = s.BOOST_TIME

    def to_dict(self) -> dict:
        """Снимок старателя."""
        return {"id": self.pid, "name": self.name,
                "x": round(self.x, 1), "y": round(self.y, 1),
                "dx": self.dir_x, "dy": self.dir_y,
                "score": self.score, "coins": self.coins,
                "boost": round(self.boost, 2)}


class Coin(Entity):
    """Обычная или золотая монета."""

    def __init__(self, cell_x: int, cell_y: int, gold: bool = False):
        super().__init__(cell_x * s.CELL + s.CELL / 2,
                         cell_y * s.CELL + s.CELL / 2, s.COIN_RADIUS)
        self.gold = gold
        self.value = s.GOLD_VALUE if gold else s.COIN_VALUE
        self.life = s.GOLD_LIFETIME if gold else None

    def update(self, dt: float) -> None:
        """Уменьшает время жизни золотой монеты."""
        if self.life is None:
            return
        self.life -= dt
        if self.life <= 0:
            self.life = 0.0
            self.alive = False

    def to_dict(self) -> dict:
        """Снимок монеты."""
        return {"x": round(self.x, 1), "y": round(self.y, 1),
                "gold": self.gold, "value": self.value,
                "life": None if self.life is None else round(self.life, 2)}

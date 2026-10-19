"""Настройки Арены."""
CELL = 40
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
MAP_W = len(MAP_ROWS[0])
MAP_H = len(MAP_ROWS)
WORLD_W = MAP_W * CELL
WORLD_H = MAP_H * CELL
PLAYER_HP = 30
PLAYER_SPEED = 160.0
PLAYER_RADIUS = 14
SHOOT_COOLDOWN = 0.35
RESPAWN_TIME = 1.5
BULLET_SPEED = 420.0
BULLET_RADIUS = 5
BULLET_DAMAGE = 10
WIN_SCORE = 3
SPAWNS = [(1, 1), (13, 7)]
COLORS = [(70, 130, 240), (235, 75, 75)]
NAMES = ["Синий", "Красный"]

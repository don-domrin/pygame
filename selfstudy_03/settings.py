"""Настройки Золотой лихорадки."""
CELL = 40
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
MAP_W = len(MAP_ROWS[0])
MAP_H = len(MAP_ROWS)
PLAYER_SPEED = 160.0
PLAYER_RADIUS = 14
BOOST_SPEED = 260.0
BOOST_TIME = 1.5
COIN_RADIUS = 10
COIN_VALUE = 1
GOLD_VALUE = 3
GOLD_CHANCE = 0.25
GOLD_LIFETIME = 5.0
COINS_ON_FIELD = 5
SPAWN_INTERVAL = 1.0
MATCH_TIME = 60.0
TABLE_SIZE = 10
SPAWNS = [(1, 1), (15, 9)]
NAMES = ["Зелёный", "Жёлтый"]

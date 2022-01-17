TOKEN_COMPLEXITY = 5

GENERATIONS = 5
OKAYMON = 10000
OKAYBALLS = 10000

WALLET_LIMIT = 6

NATURES = 2000
with open('in/natures.txt') as f:
    NATURE_NAMES = f.read().splitlines()
NATURE_DISTRIBUTION = [
    [2,1,1,1,0],
    [2,1,1,1,0],
    [2,1,1,0,1],
    [2,1,1,0,1],
    [0,2,1,1,1],
    [0,2,1,1,1],
    [0,0,2,2,1],
    [0,0,0,2,3]
]

COLORS = 10
with open('in/colors.txt') as f:
    COLOR_NAMES = f.read().splitlines()
COLOR_DISTRIBUTION = [
    360,
    320,
    280,
    240,
    200,
    200,
    160,
    120,
    80,
    40
]
COLOR_VALUES = [
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0
]
COLOR_MAP = dict(zip(COLOR_NAMES, COLOR_VALUES))

PLAYERS = 1000 # 10000

"""statistics"""
CHANCE_PLAYER_OPTS_IN = 1/3
CHANCES_PLAYER_BUYS = 1/3
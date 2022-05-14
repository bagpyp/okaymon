TOKEN_COMPLEXITY = 5

GENERATIONS = 5
OKAYMON = 10000
OKAYBALLS = 10000

WALLET_LIMIT = 6

MAX_GEN_SCORE = int(OKAYMON/GENERATIONS)

with open('in/traits.txt') as f:
    TRAIT_NAMES = f.read().splitlines()
BIG_TRAIT_NAMES = ['Item', 'Sect', 'Nature', 'Color'] # max numer of factors of 10k

PLAYERS = 10000 # 10000

"""statistics"""
# CHANCE_PLAYER_OPTS_IN = 1/5
# CHANCE_PLAYER_BUYS_AGAIN = 1/8
CHANCE_PLAYER_EXCHANGES = 1/2
CHANCE_PLAYER_EXCHANGES_AGAIN = 5/6
# NEVER GO ABOVE .5
CHANCES_PLAYER_PLAYS_STRATEGICALLY = 1/2
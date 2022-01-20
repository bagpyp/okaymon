#%%

from random import randint
from itertools import product

from data import pickle
from okayball import Okayball
from player import Player
from okaymon import Okaymon
from settings import (
    GENERATIONS,
    BIG_TRAIT_NAMES,
    OKAYMON,
    OKAYBALLS,
    TRAIT_NAMES,
    PLAYERS
)

def sample(l, n):
    s = []
    for i in range(n):
        s.append(l.pop(randint(0,len(l)-1)))
    return s

def generate_okaymon(dist):
    """traits"""
    pool = list(
        product(
            *[
                sample(TRAIT_NAMES, i) 
                for i in dist
            ]
        )
    )
    """okaymon"""
    okaymon = []
    for gen in range(GENERATIONS):
        # colors = traits[gen]["colors"]
        natures = pool.copy()
        for j in range(int(OKAYMON/GENERATIONS)):
            nature = natures.pop(randint(0,len(natures)-1))
            okaymon.append(
                Okaymon(
                    gen,
                    {
                        BIG_TRAIT_NAMES[i]:nature[i] 
                        for i in range(len(dist))
                    }
                )
            )
    pickle(okaymon)
    return okaymon

def generate_okayballs():
    """okayballs"""
    okayballs = [
        Okayball(i)
        for i in range(GENERATIONS)
        for j in range(int(OKAYBALLS/GENERATIONS))
    ]
    pickle(okayballs)
    return okayballs

def generate_players():
    players = [Player() for i in range(PLAYERS)]
    return players

if __name__ == '__main__':
    okaymon = generate_okaymon()
    okayballs = generate_okayballs()

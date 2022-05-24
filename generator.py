#%%

from random import randint
import json

from data import pickle
from okayball import Okayball
from player import Player
from okaymon import Okaymon
from settings import (
    GENERATIONS,
    OKAYBALLS,
    PLAYERS
)

def sample(l, n):
    s = []
    for i in range(n):
        s.append(l.pop(randint(0,len(l)-1)))
    return s

def generate_okaymon():
    """okaymon"""
    with open('in/okaymon.json') as f:
        jokaymon = json.loads(f.read())
    okaymon = []
    for j in jokaymon:
        gen = j.pop('gen')
        okaymon.append(Okaymon(
            gen,
            j
        ))
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

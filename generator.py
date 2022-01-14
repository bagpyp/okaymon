#%%

from random import randint
from numpy import zeros

from data import pickle
from okayball import Okayball
from player import Player
from okaymon import Okaymon
from settings import (
    GENERATIONS,
    OKAYMON,
    OKAYBALLS,
    NATURES, 
    NATURE_NAMES,
    NATURE_DISTRIBUTION,
    COLORS,
    COLOR_NAMES,
    COLOR_DISTRIBUTION,
)

def generate_okaymon():
    """natures"""
    bands = len(NATURE_DISTRIBUTION) # 8
    band_size = int(NATURES/bands) # 250
    # 2000 rows and 5 columns
    dist = zeros((NATURES,GENERATIONS)).astype(int)
    # build larger nature occurances
    for i in range(bands):
        for j in range(GENERATIONS):
            dist[
                int(i*(band_size)):int((i+1)*band_size),
                j
            ] = NATURE_DISTRIBUTION[i][j]
    chars = []
    for gen_hist in dist.T:
        cs = []
        for i,count in enumerate(gen_hist):
            for j in range(count):
                cs.append(NATURE_NAMES[i])
        chars.append(cs)
    """colors"""
    colors = [
        [COLOR_NAMES[i] for i in range(COLORS) for j in range(COLOR_DISTRIBUTION[i])]
        for k in range(GENERATIONS)
    ]
    traits = [
        {
            'colors': colors[i],
            'natures': chars[i]
        } for i in range(GENERATIONS)
    ]
    """okaymon"""
    okaymon = []
    for gen in range(GENERATIONS):
        colors = traits[gen]["colors"]
        chars = traits[gen]["natures"]
        for j in range(int(OKAYMON/GENERATIONS)):
            okaymon.append(
                Okaymon(
                    gen,
                    {
                        "color": colors.pop(randint(0,len(colors)-1)),
                        "nature": chars.pop(randint(0,len(chars)-1))
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


if __name__ == '__main__':
    okaymon = generate_okaymon()
    generate_okayballs()

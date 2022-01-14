#%%
import json
from random import randint
import pandas as pd
from pprint import pprint

from okaymon import Okaymon
from settings import GENERATIONS, CHARACTERISTICS

with open('data/traits.json') as f:
    traits = json.load(f)

okaymon = []
for gen in range(GENERATIONS):
    colors = traits[gen]["colors"]
    chars = traits[gen]["characteristics"]
    for j in range(CHARACTERISTICS):
        okaymon.append(
            Okaymon(
                gen,
                {
                    "color": colors.pop(randint(0,len(colors)-1)),
                    "characteristic": chars.pop(randint(0,len(chars)-1))
                }
            )
        )


pprint(pd.Series(okaymon).sample(100).values.tolist())



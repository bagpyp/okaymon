#%%``
import numpy as np
import pandas as pd
import json

from settings import (
    GENERATIONS,
    CHARACTERISTICS, 
    CHARACTERISTIC_DISTRIBUTION,
    COLORS,
    COLOR_DISTRIBUTION,
    COLOR_VALUES
)


"""characteristics"""

bands = len(CHARACTERISTIC_DISTRIBUTION) # 8
band_size = int(CHARACTERISTICS/bands) # 250

# 2000 rows and 5 columns

dist = np.zeros((CHARACTERISTICS,GENERATIONS)).astype(int)

# build larger characteristic occurances

for i in range(bands):
    for j in range(GENERATIONS):
        dist[
            int(i*(band_size)):int((i+1)*band_size),
            j
        ] = CHARACTERISTIC_DISTRIBUTION[i][j]

# load characteristic names

with open('in/characteristics.txt') as f:
    characteristic_names = f.read().splitlines()

chars = []
for gen_hist in dist.T:
    cs = []
    for i,count in enumerate(gen_hist):
        for j in range(count):
            cs.append(characteristic_names[i])
    chars.append(cs)


"""colors"""

with open('in/colors.txt') as f:
    color_names = f.read().splitlines()

colors = [
    [color_names[i] for i in range(COLORS) for j in range(COLOR_DISTRIBUTION[i])]
    for k in range(GENERATIONS)
]

traits = [
    {
        'colors': colors[i],
        'characteristics': chars[i]
    } for i in range(GENERATIONS)
]

color_map = {
    color_names[i]: COLOR_VALUES[i] 
    for i in range(COLORS)
}


"""data"""

# [
#     {
#         "colors": ["red", "red", "blue", ...] (2000),
#         "characteristics": ["funny", "funny", "mean", ...] (2000),
#     }, (5)
# ]
with open('data/traits.json', 'w') as f:
    json.dump(traits, f)

# {"Pearl/Diamond": 1.1, "Platinum": 1.2, ...} (10)
with open('data/colorMap.json', 'w') as f:
    json.dump(color_map, f)

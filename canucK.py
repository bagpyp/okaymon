#%%

import random

from player import Player
from okayball import Okayball


player = Player()
# make some random okayballs
okayballs = [Okayball(random.randint(0,4)) for i in range(100)]
for ball in okayballs:
  player.purchase_okayball(ball)
# p.okayballs
# [(1)', (4)', (2)', (4)', (0)', (2)', (3)', (4)', (4)', (4)']

player.okayballs
player.tokens()
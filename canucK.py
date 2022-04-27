#%%

import random
from xml.etree.ElementTree import TreeBuilder

from player import Player
from okayball import Okayball
from okaymon import Okaymon
from game import Game


player = Player()
# make some random okayballs
okayballs = [Okayball(random.randint(0,4)) for i in range(100)]
for ball in okayballs:
  player.purchase_okayball(ball)

player.okayballs
# [(1)', (4)', (2)', (4)', (0)', (2)', (3)', (4)', (4)', (4)']

player.tokens()
# [[(0)'],
#  [(1)'],
#  [(1)', (1)'],
#  [(2)'],
#  [(2)', (2)'],
#  [(2)', (2)', (2)'],
#  [(3)'],
#  [(3)', (3)'],
#  [(3)', (3)', (3)'],
#  [(3)', (3)', (3)', (3)'],
#  [(4)'],
#  [(4)', (4)'],
#  [(4)', (4)', (4)'],
#  [(4)', (4)', (4)', (4)'],
#  [(4)', (4)', (4)', (4)', (4)']]

# don't mind this nonsense
game = Game((2,5,16,25))


# our player has to be playing the game
game.players = [player]

# gonna add some available okaymon to this game
game.okaymon = [
  Okaymon(0, {"nature": "horny", "color": "purple"}),
  Okaymon(0, {"nature": "funny", "color": "red"}),
  Okaymon(1, {"nature": "puking", "color": "gravy"})
]
for okaymon in game.okaymon:
  okaymon.is_available = True

game.okaymon
# [[0], [0], [1]]

# our guy is going to buy a gen-1 okayball 
game.exchange_token(player.tokens()[0])

# the apostrophe indicates that the first gen-1 okayball is unavailable
game.okaymon
# [[0]', [0], [1]]

# it belongs now to our player
player.okaymon
# [[0]']

# but he still has the ability to buy more, because he started with lots of gen-1 balls!
player.tokens()[0]
# [(0)']

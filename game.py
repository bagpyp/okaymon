
#%% 
import random

import data
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player
from settings import CHANCE_PLAYER_OPTS_IN, CHANCES_PLAYER_BUYS

def roll(chances):
    return random.random() < chances

class Game:
    gen: int
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    players: list[Player]

    def open_okayballs(self, gen):
        for ball in filter(lambda b: b.gen == gen, self.okayballs):
            ball.is_available = True
        self.gen = gen
        data.batch_update(self.okayballs)
    def single_purchase(self, player):
        available_okayballs = [
            b for b in self.okayballs
            if b.is_available
        ]
        ball_they_want = available_okayballs[
            random.randint(0,len(available_okayballs)-1)
        ]
        if player.wallet.can_afford(ball_they_want):
            player.purchase_okayball(ball_they_want)
    def market_okayballs(self, gen):
        # some players opt in on first gen
        for p in [pp for pp in self.players if not pp.is_playing]:
            if roll(CHANCE_PLAYER_OPTS_IN):
                p.opt_in()
                #opting in means you gonna buy a ball
                self.single_purchase(p)
        for p in self.players:
            if p.is_playing:
                # buy until you roll false
                while roll(CHANCES_PLAYER_BUYS):
                    self.single_purchase(p)
    def open_okaymon(self, gen):
        for okaymon in filter(lambda b: b.gen == gen, self.okaymon):
            okaymon.is_available = True
        data.batch_update(self.okaymon)

    def __init__(self):
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon()
        self.players = generator.generate_players()

if __name__ == '__main__':
    # generate game state
    game = Game()
    # stage 0a, make gen0 okayballs available
    game.open_okayballs(0)
    # let's get these balls sold eh?
    game.market_okayballs(0)
    # stage 0b, make gen0 okaymon available
    game.open_okaymon(0)


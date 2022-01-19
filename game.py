
#%% 
import random
# from tqdm import tqdm
from collections import Counter

import data
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player
from settings import (
    GENERATIONS,
    CHANCE_PLAYER_OPTS_IN, 
    CHANCE_PLAYER_BUYS_AGAIN,
    CHANCE_PLAYER_EXCHANGES
)

# print = tqdm.write
def roll(chances):
    return random.random() < chances

class Game:
    gen: int
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    players: list[Player]
    def active_players(self):
        return [player for player in self.players if player.is_playing]
    def inactive_players(self):
        return [player for player in self.players if not player.is_playing]
    def available_okayballs(self):
        return [b for b in self.okayballs if b.is_available]
    def available_okaymon(self, gen):
        return [m for m in self.okaymon if m.gen == gen]
    def unavailable_okaymon(self):
        return [m for m in self.okaymon if not m.is_available]
    def find_player(self, player_id):
        # may need to increase token complexity
        return [p for p in self.players if p.id == player_id][0]

    def sell_okayball(self, player):
        available_okayballs = self.available_okayballs()
        if len(available_okayballs) > 0:
            ball = available_okayballs[random.randint(0,len(available_okayballs)-1)]
            if player.wallet.can_afford(ball):
                player.purchase_okayball(ball)
    def exchange_token(self, token):
        gen = token[0].gen - (len(token)-1)
        available_okaymon = self.available_okaymon(gen)
        if len(available_okaymon) > 0:
            okaymon = available_okaymon[random.randint(0,len(available_okaymon)-1)]
            self.find_player(token[0].player).exchange_token(token, okaymon)

    def open_okayballs(self):
        for ball in filter(lambda b: b.gen == self.gen, self.okayballs):
            ball.is_available = True
        data.batch_update(self.okayballs)
    def market_okayballs(self):
        print('Open season for okayballs, players are playing!')
        # players who aren't playing yet have a chance to opt in
        for p in self.inactive_players():
            if roll(CHANCE_PLAYER_OPTS_IN):
                p.opt_in()
                #opting in means you gonna buy a ball
                # TODO: maybe remove this line and increase opt in chances?
                self.sell_okayball(p)
        # for p in tqdm(self.active_players()):
        for p in self.active_players():
            # buy until you roll false
            while roll(CHANCE_PLAYER_BUYS_AGAIN):
                self.sell_okayball(p)
    def open_okaymon(self):
        for okaymon in filter(lambda b: b.gen == self.gen, self.okaymon):
            okaymon.is_available = True
        data.batch_update(self.okaymon)
    def market_okaymon(self):
        print('Players have their Okayballs, time to spend them!')
        # for p in tqdm(self.active_players()):
        for p in self.active_players():
            # need to update tokens, unless it just does is for me?
            while roll(CHANCE_PLAYER_EXCHANGES) and p.okayballs:
                tokens = p.tokens()
                random_token = tokens[random.randint(0, len(tokens)-1)]
                self.exchange_token(random_token)

    def __init__(self):
        self.gen = 0
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon()
        self.players = generator.generate_players()

    def play(self):
        print("Let the games begin!")
        for gen in range(GENERATIONS):
            print(f"Generation {gen}:")
            self.gen = gen
            self.open_okayballs()
            self.market_okayballs()
            self.open_okaymon()
            self.market_okaymon()

if __name__ == '__main__':
    game = Game()
    game.play()


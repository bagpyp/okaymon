
#%% 
import random
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

import data
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player
from settings import (
    BIG_TRAIT_NAMES,
    CHANCES_PLAYER_PLAYS_STRATEGICALLY,
    GENERATIONS,
    OKAYMON,
    CHANCE_PLAYER_OPTS_IN, 
    CHANCE_PLAYER_BUYS_AGAIN,
    CHANCE_PLAYER_EXCHANGES
)

def get_gen_from_token(token):
    return token[0].gen - (len(token)-1)
def roll(chances):
    return random.random() < chances

class Game:
    dist: tuple[int]
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
        return [p for p in self.players if p.id == player_id][0]

    # exchange utils
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

    # market actions
    def open_okayballs(self):
        for ball in filter(lambda b: b.gen == self.gen, self.okayballs):
            ball.is_available = True
        data.batch_update(self.okayballs)
    def market_okayballs(self):
        # players who aren't playing yet have a chance to opt in
        for p in self.inactive_players():
            if roll(CHANCE_PLAYER_OPTS_IN):
                p.opt_in()
                #opting in means you gonna buy a ball
                # TODO: maybe remove this line and increase opt in chances?
                self.sell_okayball(p)
        for p in tqdm(self.active_players()):
        # for p in self.active_players():
            # buy until you roll false
            while roll(CHANCE_PLAYER_BUYS_AGAIN):
                self.sell_okayball(p)
    def open_okaymon(self):
        for okaymon in filter(lambda b: b.gen == self.gen, self.okaymon):
            okaymon.is_available = True
        data.batch_update(self.okaymon)
    def market_okaymon(self):
        for p in tqdm(self.active_players()):
        # for p in self.active_players():
            # need to update tokens, unless it just does is for me?
            while roll(CHANCE_PLAYER_EXCHANGES) and p.okayballs:
                tokens = p.tokens()
                # each token corresponds to a single gen
                # if we know which gen is the rarest, we can give priorty to that gen
                # and the second!
                if roll(CHANCES_PLAYER_PLAYS_STRATEGICALLY):
                    # {2: 1993, 1: 955, 0: 816}
                    counts_left = Game.scored_okaymon(captured=False
                    ).gen.value_counts().sort_values(ascending=False
                    ).to_dict()
                    token_gens = [get_gen_from_token(t) for t in tokens]
                    # [2, 1, 0]
                    for k in counts_left.keys():
                        if k in token_gens:
                            token = tokens[token_gens.index(k)]
                            break
                else:
                    token = tokens[random.randint(0, len(tokens)-1)]
                self.exchange_token(token)

    # initializer
    def __init__(self, dist):
        self.gen = 0
        self.dist = dist
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon(self.dist)
        self.players = generator.generate_players()

    @staticmethod
    def scored_okaymon(i = 0, captured=True):
        okm = pd.read_pickle('data/okaymon.pkl')
        ok = okm[okm.is_available != captured].sort_values(by='modified')
        if i:
            ok = ok.iloc[:i+1,:]
        maximum = int(OKAYMON/GENERATIONS) + 1 # 2001
        score = maximum - ok.gen.map(dict(ok.gen.value_counts()))
        for c in [c for c in ok.columns if c in BIG_TRAIT_NAMES and c != 'Sect']:
            nunique = ok[c].nunique() # 25
            if nunique:
                maximum= int(OKAYMON/nunique) + 1 # 401
                score += maximum - ok[c].map(dict(ok[c].value_counts()))
        ok['score'] = score
        bigger_sect = ok.Sect.value_counts().idxmax()
        ok.loc[ok.Sect == bigger_sect, 'score'] += 1
        return ok
    
    # main
    def play(self):
        print("Let the games begin!")
        for gen in range(GENERATIONS):
            if gen == 2:
                # after you break here, put a break at tokens = p.tokens()
                brrrreak = True
            print(f"Generation {gen}:")
            self.gen = gen
            self.open_okayballs()
            self.market_okayballs()
            self.open_okaymon()
            self.market_okaymon()

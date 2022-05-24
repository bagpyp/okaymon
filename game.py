
#%% 
import random
from tqdm import tqdm
import pandas as pd

import data
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player
from settings import (
    BIG_TRAIT_NAMES,
    CHANCES_PLAYER_PLAYS_STRATEGICALLY,
    EXTRA_ROUNDS,
    GENERATIONS,
    OKAYMON,
    CHANCE_PLAYER_OPTS_IN, 
    CHANCE_PLAYER_BUYS_AGAIN,
    CHANCE_PLAYER_EXCHANGES
)

PLAYERS_ADDED_PER_GEN = 400

def get_gen_from_token(token):
    return token[0].gen - (len(token)-1)
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
        return [p for p in self.players if p.id == player_id][0]

    # exchange utils
    def sell_okayball(self, player):
        available_okayballs = self.available_okayballs()
        if len(available_okayballs) > 0:
            ball = available_okayballs[random.randint(0,len(available_okayballs)-1)]
            if player.wallet.can_afford(ball):
                player.purchase_okayball(ball)

    def exchange_token(self, token):
        if token:
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
        while len(self.okayballs) > 0:
            for p in self.active_players():
                # buy until you roll false
                while roll(CHANCE_PLAYER_BUYS_AGAIN):
                    self.sell_okayball(p)
    def open_okaymon(self):
        for okaymon in filter(lambda b: b.gen == self.gen, self.okaymon):
            okaymon.is_available = True
        data.batch_update(self.okaymon)
    def market_okaymon(self, gens_count=True):
        for p in tqdm(self.active_players()):
        # for p in self.active_players():
            # need to update tokens, unless it just does is for me?
            while roll(CHANCE_PLAYER_EXCHANGES) and p.okayballs:
                tokens = p.tokens()
                token = None
                # each token corresponds to a single gen
                # if we know which gen is the rarest, we can give priorty to that gen
                # and the second!
                if gens_count and roll(CHANCES_PLAYER_PLAYS_STRATEGICALLY + self.gen/10):
                    # {2: 1993, 1: 955, 0: 816}
                    counts_left = Game.scored_okaymon(captured=False, gens_count = gens_count
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
    def __init__(self):
        self.gen = 0
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon()
        self.players = generator.generate_players()

    @staticmethod
    def scored_okaymon(i = 0, captured=True, gens_count = True):
        okm = pd.read_pickle('data/okaymon.pkl')
        ok = okm[okm.is_available != captured].sort_values(by='modified')
        if i:
            ok = ok.iloc[:i+1,:]
        maximum = int(OKAYMON/GENERATIONS) + 1 # 2001
        if gens_count:
            score = maximum - ok.gen.map(dict(ok.gen.value_counts()))
        else:
            score = ok.gen*0
        for c in [c for c in ok.columns if c in BIG_TRAIT_NAMES and c != 'Sect']:
            nunique = ok[c].nunique() # 25
            if nunique:
                maximum= int(OKAYMON/nunique) + 1 # 401
                score += maximum - ok[c].map(dict(ok[c].value_counts()))
        ok['score'] = score
        if len(ok):
            bigger_sect = ok.Sect.value_counts().idxmax()
            ok.loc[ok.Sect == bigger_sect, 'score'] += 1
        return ok
    
    # main
    def play(self, gens_count = True):
        
        for gen in range(GENERATIONS):
            print(f"gen {gen + 1}:")
            self.gen = gen
            self.open_okayballs()
            self.market_okayballs()
            self.open_okaymon() 
            self.market_okaymon(gens_count = gens_count) 
        if EXTRA_ROUNDS > 0:
            print(f'playing {EXTRA_ROUNDS} more rounds...')
            for _ in range(EXTRA_ROUNDS):
                self.market_okaymon()

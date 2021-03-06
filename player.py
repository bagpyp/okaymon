#%%
from wallet import Wallet
from okayball import Okayball
from okaymon import Okaymon
from data import Asset

class Player(Asset):
    wallet: Wallet
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    is_playing: bool

    def opt_in(self):
        self.is_playing = True

    def purchase_okayball(self, ball: Okayball):
        ball.assign_to_player(self.id)
        self.wallet.purchaseRecord[ball.gen] += 1
        self.okayballs.append(ball)
    def tokens(self):
        tokens = []
        for gen in {b.gen for b in self.okayballs}:
            gen_balls = list(filter(lambda b: b.gen == gen, self.okayballs))
            for i in range(len(gen_balls)):
                to_append = gen_balls[:min(i+1, gen+1)]
                if to_append not in tokens:
                    tokens.append(to_append)
        return tokens
    def exchange_token(self, token: list[Okayball], okaymon: Okaymon):
        okaymon.assign_to_player(self.id)
        self.okaymon.append(okaymon)
        for okayball in token:
            self.okayballs.pop(
                self.okayballs.index(okayball)
            )
            okayball.assign_to_player(None)


    def __init__(self):
        super().__init__('player')
        self.wallet = Wallet()
        self.okayballs = []
        self.okaymon = []
        self.is_playing = False
    def __repr__(self):
        return f"<{self.id}>"

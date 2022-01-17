#%%
from wallet import Wallet
from okayball import Okayball
from okaymon import Okaymon
from data import Asset

from settings import TOKEN_COMPLEXITY
from errors import AllowablePurchasesError

class Player(Asset):
    wallet: Wallet
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    is_playing: bool

    def opt_in(self):
        self.is_playing = True

    def purchase_okayball(self, ball: Okayball):
        if self.wallet.can_afford(ball):
            ball.assign_to_player(self.id)
            self.wallet.purchaseRecord[ball.gen] += 1
            self.okayballs.append(ball)
        else: 
            raise AllowablePurchasesError(self.wallet.purchaseRecord)
    def tokens(self):
        tokens = []
        for gen in {b.gen for b in self.okayballs}:
            gen_balls = list(filter(lambda b: b.gen == gen, self.okayballs))
            for i in range(len(gen_balls)):
                tokens.append(gen_balls[:min(i+1, gen+2)])
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

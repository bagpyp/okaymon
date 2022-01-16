#%%
from itertools import chain, combinations
from collections import Counter

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

    def purchase_okayball(self, ball: Okayball):
        if self.wallet.is_not_full(ball):
            ball.assign_to_player(self.id)
            self.wallet.purchaseRecord[ball.gen] += 1
            self.okayballs.append(ball)
        else: 
            raise AllowablePurchasesError(self.wallet.purchaseRecord)
    def tokens(self):
        tokens = []
        for gen in {b.gen for b in self.okayballs}:
            gen_balls = list(filter(lambda b: b.gen == gen, self.okayballs))
            for i in range(1,len(gen_balls)):
                tokens.append(gen_balls[:i])
        return tokens
    

    def __init__(self):
        super().__init__('player')
        self.wallet = Wallet()
        self.okayballs = []
        self.okaymon = []
    def __repr__(self):
        return f"<{self.id}>"

#%%
from secrets import token_hex

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
            self.update()
        else: 
            raise AllowablePurchasesError(self.wallet.purchaseRecord)
    def __init__(self):
        super().__init__('player')
        self.wallet = Wallet()
        self.okayballs = []
        self.okaymon = []
    def __repr__(self):
        return f"Player {self.id}"

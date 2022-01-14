#%%
from secrets import token_hex

from wallet import Wallet
from okayball import Okayball
from okaymon import Okaymon
from settings import TOKEN_COMPLEXITY
from errors import AllowablePurchasesError

class Player:
    id: int
    wallet: Wallet
    okayballs: list[Okayball]
    okaymon: list[Okaymon]

    def purchase_okayball(self, ball: Okayball):
        if self.wallet.has_funds(ball):
            ball.assign_to_player(self.id)
            self.wallet.purchaseRecord[ball.gen] += 1
            self.okayballs.append(ball)
        else: 
            raise AllowablePurchasesError(self.wallet.purchaseRecord)
    def __init__(self):
        self.id = token_hex(TOKEN_COMPLEXITY)
        self.wallet = Wallet()
        self.okayballs = []
        self.okaymon = []
    def __repr__(self):
        return f"Player {self.id}"

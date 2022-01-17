from data import Asset
from okayball import Okayball
from settings import WALLET_LIMIT, GENERATIONS


class Wallet(Asset):
    purchaseRecord: list[int]

    def can_afford(self, ball: Okayball) -> bool:
        return self.purchaseRecord[ball.gen] < WALLET_LIMIT

    def __init__(self) -> None:
        super().__init__('wallet')
        self.purchaseRecord = [0] * GENERATIONS
    def __repr__(self) -> str:
        return f"{self.id}: {self.purchaseRecord}"



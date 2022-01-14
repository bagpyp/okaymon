from secrets import token_hex

from okayball import Okayball
from settings import WALLET_LIMIT, GENERATIONS


class Wallet:
    address: str
    purchaseRecord: list[int]

    def has_funds(self, ball: Okayball) -> bool:
        return self.purchaseRecord[ball.gen] < WALLET_LIMIT

    def __init__(self) -> None:
        # for testing, generate a len-42 hexdec
        self.address = "0x" + token_hex(21)
        self.purchaseRecord = [0] * GENERATIONS
    def __repr__(self) -> str:
        return f"{self.address}\n{self.purchaseRecord}"



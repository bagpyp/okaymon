from secrets import token_hex

from settings import TOKEN_COMPLEXITY

class Okayball:
    id: int
    gen: int
    player: int
    
    def assign_to_player(self, player_id: int) -> None:
        self.player = player_id

    def __init__(self, gen: int) -> None:
        self.id = token_hex(TOKEN_COMPLEXITY)
        self.gen = gen
        self.player = 0
    def __repr__(self) -> str:
        at = f" at {self.player}" if self.player else ""
        return f"({self.gen})" + at

class OkayballAvailabilityError(Exception):
    def __init__(self, ball: Okayball) -> None:
        self.message = f"Okayball {ball} is Unavailable."
        super().__init__()

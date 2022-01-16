from data import Asset

class Okayball(Asset):
    gen: int
    player: str
    is_available: bool

    def assign_to_player(self, player_id: str) -> None:
        self.player = player_id
        self.update()

    def __init__(self, gen: int) -> None:
        super().__init__('okayball')
        self.is_available = False
        self.gen = gen
        self.player = None
    def __repr__(self) -> str:
        return f"({self.gen})" + ('' if self.is_available else "'")

from data import Asset
from settings import COLOR_MAP

class Okaymon(Asset):
    gen: int
    player: str
    nature: str
    color: str
    color_value: int
    is_available: bool
    
    def assign_to_player(self, player_id: str) -> None:
        self.player = player_id

    def __init__(self, gen: int, traits: object):
        super().__init__('okaymon')
        # traits: {"nature": str, "color": str}
        self.gen = gen
        self.player = 0
        self.nature = traits['nature']
        self.color = traits['color']
        self.color_value = COLOR_MAP[self.color]
        self.is_available = False
    def __repr__(self):
        at = f"at {self.player} " if self.player else ""
        return f"Gen {self.gen} Okaymon ({self.id}) {at}of nature \"{self.nature}\" holding a {self.color} item"

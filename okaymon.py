from data import Asset

class Okaymon(Asset):
    gen: int
    player: str
    # nature: str
    # color: str
    # color_value: int
    is_available: bool
    
    def assign_to_player(self, player_id: str) -> None:
        self.player = player_id
        self.is_available = False
        self.update()
        
    def __init__(self, gen: int, traits: object):
        # traits: {"nature": str, "color": str}
        super().__init__('okaymon')
        self.gen = gen
        self.player = None
        for k,v in traits.items():
            setattr(self, k, v)
        # self.nature = traits['nature']
        # self.color = traits['color']
        # self.color_value = COLOR_MAP[self.color]
        self.is_available = False
    def __repr__(self):
        at = f"at {self.player} " if self.player else ""
        return f"[{self.gen}]" + ('' if self.is_available else "'")

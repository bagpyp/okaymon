from data import Asset

class Okaymon(Asset):
    gen: int
    player: str
    is_available: bool
    
    def assign_to_player(self, player_id: str) -> None:
        self.player = player_id
        self.is_available = False
        self.update()
        
    def __init__(self, gen: int, traits: object):
        super().__init__('okaymon')
        self.gen = gen
        self.player = None
        for k,v in traits.items():
            setattr(self, k, v)
        self.is_available = True
    def __repr__(self):
        at = f"at {self.player} " if self.player else ""
        return f"[{self.gen}]" + ('' if self.is_available else "'")

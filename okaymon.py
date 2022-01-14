from secrets import token_hex
import json

from settings import TOKEN_COMPLEXITY

with open('data/colorMap.json') as f:
    color_map = json.loads(f.read())

class Okaymon:
    id: int
    gen: int
    player: int
    characteristic: str
    color: str
    color_value: int
    def __init__(self, gen: int, traits: object):
        """
        # traits
        {
            "characteristic": str,
            "color": str
        }
        """
        self.id = token_hex(TOKEN_COMPLEXITY)
        self.gen = gen
        self.player = 0
        self.characteristic = traits['characteristic']
        self.color = traits['color']
        self.color_value = color_map[self.color]
    def __repr__(self):
        at = f"at {self.player} " if self.player else ""
        return f"Gen {self.gen} Okaymon ({self.id}) {at}of nature \"{self.characteristic}\" holding a {self.color} item"

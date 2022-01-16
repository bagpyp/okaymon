#%% 
import data
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player

class Game:
    gen: int
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    players: list[Player]

    def open_balls(self, gen):
        for ball in filter(lambda b: b.gen == gen, self.okayballs):
            ball.is_available = True
        self.gen = gen
        data.batch_update(self.okayballs)
    def open_okaymon(self, gen):
        for okaymon in filter(lambda b: b.gen == gen, self.okaymon):
            okaymon.is_available = True
        data.batch_update(self.okaymon)

    def __init__(self):
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon()
        self.players = generator.generate_players()

if __name__ == '__main__':
    print('let the games begin!')
    game = Game()
    print(game.okayballs[:5])
    print(game.okaymon[:5])
    game.open_balls(0)

#%% 
import generator
from okayball import Okayball
from okaymon import Okaymon
from player import Player

class Game:
    okayballs: list[Okayball]
    okaymon: list[Okaymon]
    players: list[Player]
    def __init__(self):
        self.okayballs = generator.generate_okayballs()
        self.okaymon = generator.generate_okaymon()
        

if __name__ == '__main__':
    print('let the games begin!')
    game = Game()
    print(game.okayballs[:5])
    print(game.okaymon[:5])

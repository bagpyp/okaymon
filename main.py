#%%
from game import Game
from plot import plot

gens_count = False

if __name__ == '__main__':
    game = Game()
    game.play(gens_count=gens_count)
    plot(gens_count=gens_count)
    
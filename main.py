#%%
from game import Game
from plot import plot

if __name__ == '__main__':
    game = Game()
    game.play(gens_count=True)
    plot(gens_count=True)
    
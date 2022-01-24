#%%
import pandas as pd
import matplotlib.pyplot as plt
from game import Game
from plot import plot


if __name__ == '__main__':
    # distribution
    game = Game((20,100))
    game.play()
    ok = Game.scored_okaymon()
    ok.groupby('gen').score.hist(bins=50)
    plot()
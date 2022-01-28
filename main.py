#%%
import pandas as pd
import matplotlib.pyplot as plt
from game import Game
from plot import plot


if __name__ == '__main__':
    # distribution: choose an array of numbers whose product is 2000
    game = Game((2,5,16,25))
    game.play()
    ok = Game.scored_okaymon()
    ok.groupby('gen').score.hist(bins=50)
    plot()
    
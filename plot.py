from settings import BIG_TRAIT_NAMES, OKAYMON, GENERATIONS
from game import Game
import matplotlib.pyplot as plt
import pandas as pd

def plot(evos=0):
    okm = pd.read_pickle('data/okaymon.pkl')
    ok = okm[okm.is_available == False]
    if evos:
        for i in range(0,int(len(ok)),evos):
            df = Game.scored_okaymon(i)
            df.groupby('gen').score.hist(bins=50)
            plt.pause(.01)
            plt.gcf().clear()
    else:
        ok = Game.scored_okaymon()
        ok.groupby('gen').score.hist(bins=50)
        plt.pause(.1)
        plt.gcf().clear()
        for i,g in ok.groupby('gen'):
            g.set_index('modified').sort_index().score.plot()
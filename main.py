#%%
import pandas as pd
import matplotlib.pyplot as plt
from game import Game

if __name__ == '__main__':
    # distribution
    Game((20,100)).play()
    okm = pd.read_pickle('data/okaymon.pkl')
    ok = okm[okm.is_available == False]
    ok = Game.scored_okaymon()
    ok.groupby('gen').score.hist(bins=50)
    plt.pause(.1)
    plt.gcf().clear()
    for i,g in ok.groupby('gen'):
        g.set_index('modified').sort_index().score.plot()
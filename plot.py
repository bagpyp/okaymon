#%%
from game import Game
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_rows = 100

okb = pd.read_pickle('data/okayball.pkl')
okb = okb[~okb.is_available].sort_values(by='modified')
spent_okb = okb[okb.player.isna()]
left_okb = okb[okb.player.notna()]
ok = Game.scored_okaymon()

def plot_evos(evos=0):
    ok = Game.scored_okaymon()
    if evos:
        for i in range(0,int(len(ok)),evos):
            df = Game.scored_okaymon(i)
            df.groupby('gen').score.hist(bins=50)
            plt.pause(.01)
            plt.gcf().clear()
    else:
        ok.groupby('gen').score.hist(bins=50)
        plt.pause(.01)
        plt.gcf().clear()
        for i,g in ok.groupby('gen'):
            print(i)
            g.set_index('modified').sort_index().score.plot()

plt.figure(figsize=(10,10))
plt.subplot(221)
plt.bar(ok.gen.unique(),ok.groupby('gen').score.mean())
plt.subplot(222)
plt.plot(
    list(range(5)),
    spent_okb.groupby('gen').is_available.count().values,
    label = 'unspent okayballs by gen'
    )

plt.show()
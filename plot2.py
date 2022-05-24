#%%
from game import Game
import matplotlib.pyplot as plt

def plot(evos=0):
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

if __name__ == '__main__':
    plot(1000)
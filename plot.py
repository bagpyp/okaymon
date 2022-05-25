#%%

from game import Game
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_rows = 100
pd.options.display.width = 180
def plot(gens_count = True):

  ok = Game.scored_okaymon(gens_count = gens_count)

  fig, axes = plt.subplots(5,2)
  fig.set_size_inches(40,20)
  for i,char in enumerate([
    'gen',
    'Nature',
    'Color',
    'Item',
    'Sect',
  ]):
    ok.groupby(char).score.hist(
      bins=100, 
      ax = axes[i,0]
    )
    axes[i,0].set_title(f"final score distribution per {char}")
    axes[i,0].legend(
      sorted(ok[char].unique()),
      loc=("upper left","upper right")[i%2==0]
    )


    for j,(n,g) in enumerate(ok.groupby(char)):
      g.set_index('modified').sort_index().score.plot(
        ax = axes[i,1],
        style=['-','--','-.',':'][:min(4,ok[char].nunique())][j%4]
      )
    axes[i,1].set_title(f"score over time per {char}")
    axes[i,1].legend(
      sorted(ok[char].unique()),
      loc=("upper left","upper right")[i%2!=0]
    )
    axes[i,1].set_xticklabels([])
    
  plt.savefig('data/plot.png')

def refine_to_gen(up_to_gen: int):
  ok = Game.scored_okaymon()
  return ok[ok.modified < ok[ok.gen == up_to_gen + 1]
    .reset_index()
    .sort_values('modified')
    .loc[0,'modified']]

done = []
n = 10 
ids = Game.scored_okaymon(n-1).index.unique()
ok = refine_to_gen(0)
times = ok.modified.unique()
ranks = [[-1]*len(times)]*n
for i, time in enumerate(times):
  if i == 0: continue
  ok_slice = Game.scored_okaymon(i)
  for j,id in enumerate(ids):
    if id in ok_slice.index and f"{i}-{j}" not in done:
      ranks[j][i] = ok_slice.sort_values(by='score').index.tolist().index(id)
    else:
      ranks[j][i] = -1
    done.append(f"{i}-{j}")
ranks = np.array(ranks)

pd.DataFrame(np.array(ranks).T, index=times).plot()

plot()

#%%

from game import Game
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

pd.options.display.max_rows = 100
pd.options.display.width = 180


def get_times_and_ranks(n, up_to_gen, gens_count):
  # n = 100
  # up_to_gen = 1
  done = []
  ids = Game.scored_okaymon(n-1, gens_count=gens_count).index.unique()
  ok = Game.scored_okaymon(gens_count=gens_count)
  if up_to_gen != 5:
    ok = ok[ok.modified < ok[ok.gen == up_to_gen]
            .reset_index()
            .sort_values('modified')
            .loc[0, 'modified']]
  times = ok.modified.unique()
  ranks = [[None for _ in range(len(times))] for __ in range(n)]
  print('building cyclomatic leaderboard graph ')
  for i, _ in tqdm(enumerate(times)):
    if i == 0:
      continue
    ok_slice = Game.scored_okaymon(i, gens_count=gens_count)
    for j, id in enumerate(ids):
      if id in ok_slice.index and f"{i}-{j}" not in done:
        ranks[j][i] = ok_slice.sort_values(
            by='score', ascending=False).index.tolist().index(id)
      else:
        continue
      done.append(f"{i}-{j}")
  ranks = np.array(ranks)
  ranks[0][0] = 0
  return [times, ranks]


def plot(gens_count):

  ok = Game.scored_okaymon(gens_count=gens_count)

  fig, axes = plt.subplots(6, 2, gridspec_kw = {
    'width_ratios': [1, 1],
    'height_ratios': [1, 1, 1, 1, 1, 3],
    # 'wspace': 0.5,
    'hspace': 0.5}
  )

  fig.set_size_inches(40, 20)
  for i, char in enumerate([
      'gen',
      'Nature',
      'Color',
      'Item',
      'Sect',
  ]):
    ok.groupby(char).score.hist(
        bins=100,
        ax=axes[i, 0]
    )
    axes[i, 0].set_title(f"final score distribution per {char}")
    axes[i, 0].legend(
        sorted(ok[char].unique()),
        loc=("upper left", "upper right")[i % 2 == 0]
    )

    for j, (n, g) in enumerate(ok.groupby(char)):
      g.set_index('modified').sort_index().score.plot(
          ax=axes[i, 1],
          style=['-', '--', '-.', ':'][:min(4, ok[char].nunique())][j % 4]
      )
    axes[i, 1].set_title(f"score over time per {char}")
    axes[i, 1].legend(
        sorted(ok[char].unique()),
        loc=("upper left", "upper right")[i % 2 != 0]
    )
    axes[i, 1].set_xticklabels([])
  for square, pair in {0: (10, 5), 1: (50, 1)}.items():
    times, ranks = get_times_and_ranks(pair[0], pair[1], gens_count=gens_count)
    axes[5, square].plot(times, ranks.T)
    axes[5, square].set_title(
        f"first {pair[0]} players leaderboard travel through gen {pair[1]}")
    if square == 0:
      axes[5, square].legend(list(range(1,pair[0]+1)))

  plt.savefig('data/plot.png')

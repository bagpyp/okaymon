
#%%
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep

from settings import MAX_NATURE_SCORE, MAX_GEN_SCORE

okb = pd.read_pickle('data/okayball.pkl')
okm = pd.read_pickle('data/okaymon.pkl')

ok = okm[okm.is_available == False].sort_values(by='modified')

def score_okaymon(df):
    score = df.nature.map(dict(df.nature.value_counts()*-1 + MAX_NATURE_SCORE + 1))
    score *= df.gen.map(dict(df.gen.value_counts()*-1 + MAX_GEN_SCORE + 1))
    score *= df.color_value
    return score

score = score_okaymon(ok)

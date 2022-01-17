
#%%
import pandas as pd
import matplotlib.pyplot as plt

okb = pd.read_pickle('data/okayball.pkl')
okm = pd.read_pickle('data/okaymon.pkl')

# hist of how many okayballs playets have
okb[~okb.is_available].groupby('player').gen.count().hist()


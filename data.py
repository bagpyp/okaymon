import pandas as pd
import datetime as dt
from secrets import token_hex

from settings import TOKEN_COMPLEXITY

def path(type):
    return f"data/{type}.pkl"

class Asset:
    id: str
    created: dt.datetime
    modified: dt.datetime
    type: str
    def __init__(self, type):
        self.__dict__['type'] = type
        self.__dict__['id'] = token_hex(TOKEN_COMPLEXITY)
        self.__dict__['created'] = dt.datetime.now()
        self.__dict__['modified'] = dt.datetime.now()
    def __setattr__(self, __name, __value):
        self.__dict__[__name] = __value
        self.__dict__['modified'] = dt.datetime.now()
        # read pickle
        tmp = pd.read_pickle(
            path(self.type)
        )
        # update state
        tmp.loc[self.id, __name] = __value 
        tmp.loc[self.id, 'modified'] = dt.datetime.now()
        # persist
        tmp.to_pickle(
            path(self.type)
        )

def pickle(assets: list[Asset]):
    pd.DataFrame(
        [a.__dict__ for a in assets]
    ).set_index(
        'id'
    ).to_pickle(
        path(assets[0].type)
    )

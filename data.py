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
        self.type = type
        self.id = token_hex(TOKEN_COMPLEXITY)
        self.created = dt.datetime.now()
        self.modified = dt.datetime.now()

    def update(self):
        # read pickle
        tmp = pd.read_pickle(
            path(self.type)
        )
        # update state
        self.modified = dt.datetime.now()
        for k, v in self.__dict__.items():
            if k != 'id':
                tmp.loc[self.id, k] = v
        # persist
        tmp.to_pickle(
            path(self.type)
        )

def pickle(assets: list[Asset]):
    pd.DataFrame(
        [
            a.__dict__
            for a in assets
        ]
    ).set_index(
        'id'
    ).to_pickle(
        path(
            assets[0].type
        )
    )

def batch_update(assets: list[Asset]):
    df = pd.read_pickle(
        path(
            assets[0].type
        )
    )
    update = pd.DataFrame(
            [
                a.__dict__
                for a in assets
            ]
        ).set_index(
            'id'
        )
    # update.modified = dt.datetime.now()
    df.update(
        update
    )
    df.to_pickle(
        path(
            assets[0].type
        )
    )

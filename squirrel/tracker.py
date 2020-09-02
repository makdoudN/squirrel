import numpy as np
import collections


class Tracker:
    def __init__(self, decimals=4):
        self.decimals = decimals
        self.buf = collections.defaultdict(list)

    def log(self, kwargs: dict, reset: bool = False):
        for k, v in kwargs.items():
            v = np.around(v, self.decimals)
            if reset:
                self.buf[k].clear()
            self.buf[k].append(v)

    def summary(self):
        out = {}
        for k, v in self.buf.items():
            out[k] = np.mean(v)
        self.buf.clear()
        return out

    def __getitem__(self, item: str):
        return self.buf[item]

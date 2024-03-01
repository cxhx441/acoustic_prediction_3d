from sympy import Point
from Source import Source
from Barrier import Barrier


class Receiver():
    def __init__(self, geo: Point,
                 name: str = None,
                 dBA_limit: float = None,
                 dBA_predictied: float = None
                ) -> None:
        self.geo = geo
        self.affecting_sources = set()  # set of sources that affect this receiver
        self.source_barrier_pairs = set()  # set of tuples of (source, barrier) pairs.
        self.name = name
        self.dBA_limit = dBA_limit
        self.dBA_predicted = dBA_limit
        self.source_barriers = []

    def add_source_barrier(self, s: Source, b: Barrier|None):
        self.source_barrier[s.id] = b.id

    def remove_source(self, s: Source):
        try:
            del self.source_barrier[s.id]
        except:
            pass


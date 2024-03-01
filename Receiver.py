from sympy import Point


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

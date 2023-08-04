from sympy import Point


class Receiver():
    def __init__(self, point: Point) -> None:
        self.point = point
        self.affecting_sources = set()  # set of sources that affect this receiver
        self.source_barrier_pairs = set()  # set of tuples of (source, barrier) pairs.
        self.dBA = 0  # the dBA level at this receiver

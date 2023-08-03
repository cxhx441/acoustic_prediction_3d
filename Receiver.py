from sympy import Point


class Receiver(Point):
    def __init__(self, point: Point) -> None:
        super().__init__(point.x, point.y, point.z)
        self.affecting_sources = set()  # set of sources that affect this receiver
        self.source_barrier_pairs = set()  # set of tuples of (source, barrier) pairs.
        self.dBA = 0  # the dBA level at this receiver

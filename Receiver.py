from Geometry import Coordinate


class Receiver(Coordinate):
    def __init__(self, coords: Coordinate) -> None:
        super().__init__(coords.x, coords.y, coords.z)
        self.affecting_sources = set()  # set of sources that affect this receiver
        self.source_barrier_pairs = set()  # set of tuples of (source, barrier) pairs.
        self.dBA = 0  # the dBA level at this receiver

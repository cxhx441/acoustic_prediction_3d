from sympy import Segment


class Barrier:
    def __init__(self, segment: Segment) -> None:
        self.segment = segment

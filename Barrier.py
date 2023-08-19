from sympy import Segment


class Barrier:
    def __init__(self, geo: Segment) -> None:
        self.geo = geo

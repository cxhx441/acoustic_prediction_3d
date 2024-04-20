from sympy import Segment

class Barrier:
    def __init__(self,
                 geo:   Segment,
                 name:  str = None
                ) -> None:
        self.geo = geo
        self.name = name
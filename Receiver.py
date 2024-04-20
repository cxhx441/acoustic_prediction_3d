from sympy import Point

class Receiver():
    def __init__(self,
                 geo:           Point,
                 name:          str =   None,
                 dBA_limit:     float = None,
                 dBA_predicted: float = None
                ) -> None:
        self.geo =              geo
        self.name =             name
        self.dBA_limit =        dBA_limit
        self.dBA_predicted =    dBA_predicted
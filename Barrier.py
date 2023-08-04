from sympy import Segment


class Barrier(Segment):
    def __init__(self, *args) -> None:
        if len(args) == 1:
            try:
                super().__init__(args[0].p1, args[0].p2)
            except AttributeError:
                raise TypeError("args must be 2 Point objects or 1 Line object")

        elif len(args) == 2:
            try:
                super().__init__(args[0], args[1])
            except AttributeError:
                raise TypeError("args must be 2 Point objects or 1 Line object")

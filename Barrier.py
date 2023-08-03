from Source import Source  # for type hinting
from Receiver import Receiver  # for type hinting
from sympy import Segment
from acoustics.decibel import dbsum
import insertion_loss_methods as il_methods

DEBUG = True


def log(*args):
    if DEBUG:
        print(*args)


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

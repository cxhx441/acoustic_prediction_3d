from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from InsertionLoss import InsertionLoss
from math import log10, sqrt
import sympy

class App:
    def __init__(self):
        self.sources = set()
        self.receivers = set()
        self.barriers = set()
        self.directivity = set() # (s, r)
        self.ignore = set() # (s, r)

    # adders
    def add_source(self, s: Source):
        self.sources.add(s)

    def add_receiver(self, r: Receiver):
        self.receivers.add(r)

    def add_barrier(self, b: Barrier):
        self.barriers.add(b)

    # removers
    def remove_source(self, s: Source):
        if s in self.sources:
            self.sources.remove(s)
        for r in self.receivers:
            r.remove_source(s)
            if (s, r) in self.directivity:
                self.directivity.remove((s, r))
            if (s, r) in self.ignore:
                self.ignore.remove((s, r))
        for b in self.barriers:
            b.remove_source(s)

    def remove_receiver(self, r: Receiver):
        if r in self.receivers:
            self.receivers.remove(r)
        for s in self.sources:
            s.remove_receiver(r)
            if (s, r) in self.directivity:
                self.directivity.remove((s, r))
            if (s, r) in self.ignore:
                self.ignore.remove((s, r))
        for b in self.barriers:
            b.remove_receiver(r)

    def remove_barrier(self, b: Barrier):
        if b in self.barriers:
            self.barriers.remove(b)
        for r in self.receivers.values():
            r.remove_barrier(b)

    def update_dBA_predictions(self, r: Receiver|None):
        if r is not None:
            for rec in self.receivers:
                self.update_predictions(rec)
            return

        overall_pressure = 0
        for s in r.affecting_sources:
            # IGNORE
            if (s, r) in self.ignore:
                continue


            # SOUND POWER
            LwA = s.dBA
            if s.ref_dist != 0:
                q = s.q_tested
                r = (s.ref_dist/3.28)
                pi = 3.14159265359
                LwA = s.dBA + abs(10*log10(( q / ( 4 * pi * (r**2) ) ) ) )

            # DISTANCE LOSS
            distance_ft = s.geo.distance(r.geo)
            distance_m = distance_ft / 3.28
            r = distance_m
            distance_loss = 10*log10( q / ( 4 * pi * (r**2) ) )

            # BARRIER LOSS
            b_used = None
            b_il = 0
            for b in self.barriers:
                if (s, r) in b.s_r_combos:
                    b_used = b
            if b_used is not None:
                b_il = InsertionLoss(s, r, b_used)

            # DIRECTIVITY LOSS
            directivity_loss = 0
            if (s, r) in self.directivity:
                directivity_loss = self.directivity[(s, r)]

            dBA = LwA + distance_loss + b_il + directivity_loss
            overall_pressure += 10**(dBA)

        r.dBA_predicted = 20*log10(overall_pressure)


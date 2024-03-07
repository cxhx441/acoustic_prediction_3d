from sympy import Segment


class Barrier:
    def __init__(self, geo: Segment,
                 name: str = None
                ) -> None:
        self.geo = geo
        self.name = name
        self.s_r_combos = set()

    def add_s_r_combo(self, s: Source, r: Receiver):
        self.s_r_combos.add((s, r))

    def remove_source(self, s: Source):
        to_remove = list()
        for s_r_combo in self.s_r_combos:
            if s == s_r_combo[0]:
                to_remove.append(s_r_combo)
        for s_r_combo in to_remove:
            self.s_r_combos.remove(s_r_combo)

    def remove_receiver(self, r: Receiver):
        to_remove = list()
        for s_r_combo in self.s_r_combos:
            if r == s_r_combo[1]:
                to_remove.append(s_r_combo)
        for s_r_combo in to_remove:
            self.s_r_combos.remove(s_r_combo)



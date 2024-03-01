from Source import Source
from Receiver import Receiver
from Barrier import Barrier

class AssociationMatrix:
    def __init__(self):
        self.s2r = dict()
        self.r2s = dict()

    def associate(self, s: Source, r: Receiver, b: Barrier|None):
        if s.id in self.s2r:
            self.s2r[s.id][r.id] = b.id
        else:
            self.s2r[s.id] = {r.id: b.id}

        if r.id in self.r2s:
            self.r2s[r.id][s.id] = b.id
        else:
            self.r2s[r.id] = {s.id: b.id}

    def de_associate(self, s: Source, r: Receiver):
        try:
            del self.s2r[s.id][r.id]
        except:
            pass

        try:
            del self.r2s[r.id][s.id]
        except:
            pass

    def remove_source(self, s: Source):
        try:
            del self.s2r[s.id]
        except:
            pass

        for r in self.r2s:
            try:
                del self.r2s[r.id][s.id]
            except:
                pass

    def remove_receiver(self, r: Receiver):
        try:
            del self.r2s[r.id]
        except:
            pass

        for s in self.s2r:
            try:
                del self.s2r[s.id][r.id]
            except:
                pass

    def remove_barrier(self, b: Barrier):
        for r in self.r2s:
            for s in self.s2r:
                try:
                    if b.id == self.s2r[s.id][r.id]:
                        self.s2r[s.id][r.id] = None
                except:
                    pass
                try:
                    if b.id == self.r2s[r.id][r.id]:
                        self.r2s[r.id][s.id] = None
                except:
                    pass


class Map:
    def __init__(self):
        self.sources = dict()
        self.receivers = dict()
        self.barriers = dict()
        self.association = AssociationMatrix()

    # adders
    def add_source(self, s: Source):
        self.sources[s.id] = s

    def add_receiver(self, r: Receiver):
        self.receivers[r.id] = r

    def add_barrier(self, b: Barrier):
        self.barriers[b.id] = b

    # removers
    def remove_source(self, s: Source):
        del self.sources[s.id]
        self.association.remove_source(s)

    def remove_receiver(self, r: Receiver):
        del self.receivers[r.id]
        self.association.remove_receiver(r)

    def remove_barrier(self, b: Barrier):
        del self.barriers[b.id]
        self.association.remove_barrier(b)

    
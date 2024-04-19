from Source import Source
from Receiver import Receiver
from Barrier import Barrier

class Map:
    def __init__(self):
        self.sources = dict()
        self.receivers = dict()
        self.barriers = dict()

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
        for r in self.receivers.values():
            for receiver_s_id in r.source_barriers:
                r._remove_source(self.receivers[receiver_s_id])

    def remove_receiver(self, r: Receiver):
        del self.receivers[r.id]

    def remove_barrier(self, b: Barrier):
        del self.barriers[b.id]
        for r in self.receivers.values():
            for s_id in r.source_barriers:
                r.add_source_barrier(self.receivers[s_id], None)



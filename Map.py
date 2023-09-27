from Source import Source
from Receiver import Receiver
from Barrier import Barrier

class Map:
    def __init__(self): 
        self.sources = set()
        self.receivers = set()
        self.barriers = set()

        # self.source_associations = dict() # {"source_id": set(("receiver_id", "barrier_id"))}
        # self.receiver_associations = dict() # {"receiver_id": set(("source_id", "barrier_id"))}
        # self.barrier_associations = dict() # {"barrier_id": set(("source_id", "receiver_id"))}

        self.ignore_matrix = dict() 
        self.barrier_association_matrix = dict()

    # adders
    def add_source(self, s: Source): 
        self.sources.add(s)

    def add_receiver(self, r: Receiver): 
        self.receivers.add(r)
    
    def add_barrier(self, b: Barrier): 
        self.barriers.add(b)

    # removers
    def remove_source(self, s: Source): 
        self.sources.remove(s)

    def remove_receiver(self, r: Receiver): 
        self.receivers.remove(r)
    
    def remove_barrier(self, b: Barrier): 
        self.barriers.remove(b)

    def associate(self, s: Source, r: Receiver, b: Barrier): 
        # TODO check if s-r already has b, if so, remove that association. 
        # TODO might need hashed/unique IDs for s/r/b objects for better identification. 

        # conditions
            # s and r same changing b
            # s and b same changing r
        if s.id in self.source_associations and (r.id, b.id) in self.source_associations[s.id]:
            self.source_association[s.id].remove((r.id, b.id))
        if r.id in self.receiver_associations and (s.id, b.id) in self.receiver_associations[r.id]:
            self.receiver_association[r.id].remove((s.id, b.id))
        if b.id in self.barrier_associations and (s.id, r.id) in self.barrier_associations[b.id]:
            self.barrier_association[b.id].remove((s.id, r.id))
        
        self.source_association[s.id].add((r.id, b.id))
        self.receiver_association[r.id].add((s.id, b.id))
        self.barrier_association[b.id].add((s.id, r.id))

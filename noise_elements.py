import math
from geometric_elements import Point, Line


class Source(Point):
    def __init__(self, coords, dBA, reference_distance: float) -> None:
        self.dBA = dBA  # the dBA level of this source
        self.reference_distance = (
            reference_distance  # the reference distance of this source in ft
        )

        self.affected_receivers = set()  # set of receivers affected by this source
        self.receiver_barrier_pairs = (
            set()
        )  # set of tuples of (receiver, barrier) pairs.

    def add_affected_receiver(self, r: "Receiver"):
        self.affected_receviers.add(r)

    def remove_affected_receiver(self, r: "Receiver"):
        self.affected_receivers.remove(r)


class Receiver(Point):
    def __init__(self, coords) -> None:
        self.affecting_sources = set()  # set of sources that affect this receiver
        self.source_barrier_pairs = set()  # set of tuples of (source, barrier) pairs.
        self.dBA = 0  # the dBA level at this receiver

    def add_affecting_source(self, s: Source):
        self.affecting_sources.add(s)

    def remove_affecting_source(self, s: Source):
        self.affecting_sources.remove(s)


class Barrier(Line):
    def __init__(self, start_coords, end_coords) -> None:
        pass


class Map:
    def __init__(self, receivers: set, sources: set, barriers: set) -> None:
        self.sources = sources
        self.receivers = receivers
        self.barriers = barriers
        self.source_receiver_combo = set()

    # getters
    def get_sources(self) -> set:
        return self.sources

    def get_receivers(self) -> set:
        return self.receivers

    def get_barriers(self) -> set:
        return self.barriers

    # setters
    def set_sources(self, sources: set):
        self.sources = sources

    def set_receivers(self, receivers: set):
        self.receivers = receivers

    def set_barriers(self, barriers: set):
        self.barriers = barriers

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

    # pair source and receiver
    def add_source_receiver_pair(self, s: Source, r: Receiver):
        s.add_affected_receiver(r)
        r.add_affecting_source(s)

    def remove_source_receiver_pair(self, s: Source, r: Receiver):
        s.remove_affected_receiver(r)
        r.remove_affecting_source(s)

    # source-receiver pair to barrier methods
    def add_source_receiver_barrier_combo(self, s: Source, r: Receiver, b: Barrier):
        """Adds a source-receiver-barrier combo to the map."""
        self.source_receiver_barrier_combo.add((s, r, b))

    def remove_source_receiver_barrier_combo(self, s: Source, r: Receiver, b: Barrier):
        """Removes a source-receiver-barrier combo from the map."""
        self.source_receiver_combo.remove((s, r, b))

    # TODO need to check that updating a source after it is already in the receiver's affecting set, it still works. Same for barriers.

    def calculate_predicted_dBA(self, r: Receiver):
        """assign the calculated dBA to the receiver based on the afficting receivers and source-receiver pairs assigned to barriers"""
        sound_pressure_to_add = 0
        for s in self.sources:
            if s in r.affecting_sources:
                for b in self.barriers:
                    bar_TL = 0
                    if (s, r) in b.source_receiver_pairs:
                        bar_TL = b.get_insertion_loss(s, r)

                    distance = r.get_distance(s)
                    distance_loss = 20 * math.log10(distance / s.reference_distance)
                    dBA_to_add = s.dBA + distance_loss - bar_TL
                    sound_pressure_to_add += 10 ** (dBA_to_add / 10)

        r.dBA = 10 * math.log10(sound_pressure_to_add)

    def calculate_predicted_dBA_for_all_receivers(self):
        for r in self.receivers:
            self.calculate_predicted_dBA(r)

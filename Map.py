# TODO need to separate out which source/barriers/receivers are all impacting one another. coordinate when changing one source, barrier, or receiver, the others are updated accordingly.
import math
from Receiver import Receiver
from Source import Source
from Barrier import Barrier


class Map:
    def __init__(self, receivers: set, sources: set, barriers: set) -> None:
        self.sources = sources
        self.receivers = receivers
        self.barriers = barriers
        self.source_receiver_pairs = set()
        self.source_receiver_barrier_combos = set()
        self.TAKE_ARI_BARRIER = True
        self.TAKE_OB_BARRIER = True

    # getters
    def get_sources(self) -> set:
        return self.sources

    def get_receivers(self) -> set:
        return self.receivers

    def get_barriers(self) -> set:
        return self.barriers

    def get_source_receiver_pairs(self) -> set:
        return self.source_receiver_pairs

    def get_source_receiver_barrier_combo(self) -> set:
        return self.source_receiver_barrier_combos

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

    def add_source_receiver_pair(self, s: Source, r: Receiver):
        self.source_receiver_pairs.add((s, r))

    def add_source_receiver_barrier_combo(self, s: Source, r: Receiver, b: Barrier):
        self.source_receiver_barrier_combos.add((s, r, b))

    # removers
    def remove_source(self, s: Source):
        self.sources.remove(s)

    def remove_receiver(self, r: Receiver):
        self.receivers.remove(r)

    def remove_barrier(self, b: Barrier):
        self.barriers.remove(b)

    # pair source and receiver
    def add_source_receiver_pair(self, s: Source, r: Receiver):
        self.source_receiver_pairs.add((s, r))

    def remove_source_receiver_pair(self, s: Source, r: Receiver):
        self.source_receiver_pairs.remove((s, r))

    # source-receiver pair to barrier methods
    def add_source_receiver_barrier_combo(self, s: Source, r: Receiver, b: Barrier):
        self.source_receiver_barrier_combo.add((s, r, b))

    def remove_source_receiver_barrier_combo(self, s: Source, r: Receiver, b: Barrier):
        self.source_receiver_barrier_combos.remove((s, r, b))

    # TODO need to check that updating a source after it is already in the receiver's affecting set, it still works. Same for barriers.

    def get_dBA_impact(self, s: Source, r: Receiver, b: Barrier) -> float:
        if (s, r) not in self.source_receiver_pairs:
            return 0

        distance = r.get_distance(s)
        distance_loss = 20 * math.log10(distance / s.reference_distance)
        bar_TL = 0
        if (s, r, b) in self.source_receiver_barrier_combos:
            bar_TL = b.get_insertion_loss(s, r)
        dBA = s.dBA + distance_loss - bar_TL
        return dBA

    def calculate_predicted_dBA(self, r: Receiver):
        """assign the calculated dBA to the receiver based on the afficting receivers and source-receiver pairs assigned to barriers"""
        sound_pressure_to_add = 0
        for s in self.sources:
            if s in r.affecting_sources:
                distance = r.get_distance(s)
                distance_loss = 20 * math.log10(distance / s.reference_distance)
                bar_TL = 0
                for b in self.barriers:
                    if (s, r, b) in self.source_receiver_barrier_combos:
                        if (
                            self.TAKE_ARI_BARRIER is True
                            and self.TAKE_OB_BARRIER is False
                        ):
                            bar_TL = b.get_insertion_loss_ARI(s, r)[0]
                        elif (
                            self.TAKE_ARI_BARRIER is True
                            and self.TAKE_OB_BARRIER is True
                            and s.octave_bands is not None
                        ):
                            bar_TL = b.get_insertion_loss_OB_fresnel(s, r)[0]
                        break
                dBA = s.dBA + distance_loss - bar_TL
                sound_pressure_to_add += 10 ** (dBA / 10)
        r.dBA = 10 * math.log10(sound_pressure_to_add)

    def calculate_predicted_dBA_for_all_receivers(self):
        for r in self.receivers:
            self.calculate_predicted_dBA(r)

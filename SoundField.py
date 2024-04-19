from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from InsertionLoss import InsertionLoss
from math import log10, pi
import sympy

ALLOWED_BARRIER_METHODS = ('ARI', 'FRESNEL')
class SoundPath:
    def __init__(self, directivity_loss: float = 0, ignore: bool = False, allowed_barriers: set = None, barrier_method: str = 'ARI'):
        self.allowed_barriers = allowed_barriers
        if self.allowed_barriers is None: self.allowed_barriers = set()
        self.directivity_loss = directivity_loss
        self.ignore = ignore
        self.barrier_method = barrier_method
        if self.barrier_method not in ALLOWED_BARRIER_METHODS:
            raise ValueError(f'Barrier method must be one of {ALLOWED_BARRIER_METHODS}')

class SoundField:
    def __init__(self):
        self.sound_path_matrix = list()
        self.sources = list()
        self.receivers = list()
        self.barriers = list()

    # def source_idx(self, s: Source):
    #     return self.sources.index(s)
    #
    # def receiver_idx(self, r: Receiver):
    #     return self.receivers.index(r)
    #
    # def barrier_idx(self, b: Barrier):
    #     return self.barriers.index(b)

    # adders
    def add(self, srb: Source | Receiver | Barrier | set[Source | Receiver | Barrier]):
        if isinstance(srb, set):
            for el in srb:
                self.add(el)
        elif isinstance(srb, Source):
            self._add_source(srb)
        elif isinstance(srb, Receiver):
            self._add_receiver(srb)
        elif isinstance(srb, Barrier):
            self._add_barrier(srb)

    def _add_source(self, s: Source):
        self.sources.append(s)
        self.sound_path_matrix.append([SoundPath()] * len(self.receivers))

    def _add_receiver(self, r: Receiver):
        self.receivers.append(r)
        for s_i in range(len(self.sources)):
            self.sound_path_matrix[s_i].append(SoundPath())

    def _add_barrier(self, b: Barrier):
        self.barriers.append(b)

    # removers
    def remove(self, srb: Source | Receiver | Barrier | set[Source | Receiver | Barrier]):
        if isinstance(srb, set):
            for el in srb:
                self.remove(el)
        elif isinstance(srb, Source):
            self._remove_source(srb)
        elif isinstance(srb, Receiver):
            self._remove_receiver(srb)
        elif isinstance(srb, Barrier):
            self._remove_barrier(srb)
    def _remove_source(self, s: Source):
        s_target_i = self.sources.index(s)
        del self.sources[s_target_i]
        for s_i in range(len(self.sources)):
            del self.sound_path_matrix[s_i][s_target_i]

    def _remove_receiver(self, r: Receiver):
        r_target_i = self.receivers.index(r)
        del self.receivers[r_target_i]
        for r_i in range(len(self.receivers)):
            del self.sound_path_matrix[r_i][r_target_i]

    def _remove_barrier(self, b: Barrier):
        b_target_i = self.barriers.index(b)
        del self.barriers[b_target_i]
        for s_i in range(len(self.sources)):
            for r_i in range(len(self.receivers)):
                self.sound_path_matrix[s_i][r_i].allowed_barriers.remove(b)

    def set_directivity_loss(self, s: Source, r: Receiver, directivity_loss: float):
        s_i = self.sources.index(s)
        r_i = self.receivers.index(r)
        sp = self.sound_path_matrix[s_i][r_i]
        sp.directivity_loss = directivity_loss

    def set_ignore(self, s: Source, r: Receiver, ignore: bool):
        s_i = self.sources.index(s)
        r_i = self.receivers.index(r)
        sp = self.sound_path_matrix[s_i][r_i]
        sp.ignore = ignore

    def set_allowed_barriers(self, s: Source, r: Receiver, barriers: set[Barrier]):
        s_i = self.sources.index(s)
        r_i = self.receivers.index(r)
        sp = self.sound_path_matrix[s_i][r_i]
        sp.allowed_barriers = barriers

    # def add_allowed_barrier(self, s: Source, r: Receiver, b: Barrier):
    #     s_i = self.sources.index(s)
    #     r_i = self.receivers.index(r)
    #     sp = self.sound_path_matrix[s_i][r_i]
    #     sp.allowed_barriers.add(b)

    # def remove_allowed_barrier(self, s: Source, r: Receiver, b: Barrier):
    #     s_i = self.sources.index(s)
    #     r_i = self.receivers.index(r)
    #     sp = self.sound_path_matrix[s_i][r_i]
    #     sp.allowed_barriers.remove(b)

    # def add_allowed_barriers(self, s: Source, r: Receiver, barriers: set):
    #     s_i = self.sources.index(s)
    #     r_i = self.receivers.index(r)
    #     sp = self.sound_path_matrix[s_i][r_i]
    #     sp.allowed_barriers = sp.allowed_barriers | barriers

    # def remove_allowed_barriers(self, s: Source, r: Receiver, barriers: set):
    #     s_i = self.sources.index(s)
    #     r_i = self.receivers.index(r)
    #     sp = self.sound_path_matrix[s_i][r_i]
    #     sp.allowed_barriers = sp.allowed_barriers - barriers

    def set_barrier_method(self, s: Source, r: Receiver, barrier_method: str):
        if barrier_method not in ALLOWED_BARRIER_METHODS:
            raise ValueError(f'Barrier method must be one of {ALLOWED_BARRIER_METHODS}')
        s_i = self.sources.index(s)
        r_i = self.receivers.index(r)
        sp = self.sound_path_matrix[s_i][r_i]
        sp.barrier_method = barrier_method

    def update_dBA_predictions(self, r: Receiver|None = None):
        if r is None:
            for inner_r in self.receivers:
                self.update_dBA_predictions(inner_r)
            return

        sound_paths = []
        r_i = self.receivers.index(r)
        for s_i in range(len(self.sources)):
            sound_paths.append(self.sound_path_matrix[s_i][r_i])

        overall_pressure = 0
        for i in range(len(self.sources)):
            sp = sound_paths[i]
            s = self.sources[i]
            if sp.ignore is True:
                continue

            b_used, b_il = SoundField._get_best_barrier_il(s, r, sp)
            distance_ft = s.geo.distance(r.geo)
            distance_loss = s.get_distance_loss(distance_ft)
            q_effect = s.get_q_effect()

            dBA = s.dBA - distance_loss - b_il - sp.directivity_loss + q_effect

            overall_pressure += 10**(dBA/10)

        r.dBA_predicted = 10*log10(overall_pressure)

    @staticmethod
    def _get_best_barrier_il(s: Source, r: Receiver, sp: SoundPath) -> (Barrier, float):
        b_used = None
        b_il = 0
        for b in sp.allowed_barriers:
            if sp.barrier_method == 'FRESNEL':
                calculated_b_il = InsertionLoss(s, r, b).get_fresnel_il()
            else:
                calculated_b_il = InsertionLoss(s, r, b).get_ARI_il()

            if calculated_b_il > b_il:
                b_il = calculated_b_il
                b_used = b
        return b_used, b_il

    # def _check_valid_srb(self, s: Source=None, r: Receiver=None, b: Barrier=None):
    #     if s is not None and s not in self.sources:
    #         raise ValueError(f'Source {s} not in {self.sources}')
    #     if r is not None and r not in self.receivers:
    #         raise ValueError(f'Receiver {r} not in {self.receivers}')
    #     if b is not None and b not in self.barriers:
    #         raise ValueError(f'Barrier {b} not in {self.barriers}')
    #

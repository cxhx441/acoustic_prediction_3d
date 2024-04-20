from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from InsertionLoss import InsertionLoss
from math import log10, pi
from ordered_set import OrderedSet
import sympy

ALLOWED_BARRIER_METHODS = ('ARI', 'FRESNEL')
class SoundPath:
    def __init__(self,
                 directivity_loss:  float   = 0,
                 ignore:            bool    = False,
                 allowed_barriers:  set     = None,
                 barrier_method:    str     = "ARI"
                 ):
        self.directivity_loss   = directivity_loss
        self.ignore             = ignore
        self.allowed_barriers   = allowed_barriers
        self.barrier_method     = barrier_method

        if self.allowed_barriers is None:
            self.allowed_barriers = set()
        if self.barrier_method not in ALLOWED_BARRIER_METHODS:
            raise ValueError(f'Barrier method must be one of {ALLOWED_BARRIER_METHODS}')

class SoundField:
    def __init__(self):
        self.sound_path_matrix  = list()
        self.sources            = OrderedSet()
        self.receivers          = OrderedSet()
        self.barriers           = OrderedSet()

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
        if s in self.sources:
            return
        self.sources.add(s)
        self.sound_path_matrix.append([SoundPath()] * len(self.receivers))

    def _add_receiver(self, r: Receiver):
        if r in self.receivers:
            return
        self.receivers.add(r)
        for s_i in range(len(self.sources)):
            self.sound_path_matrix[s_i].append(SoundPath())

    def _add_barrier(self, b: Barrier):
        self.barriers.add(b)

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
        if s not in self.sources:
            return
        del self.sound_path_matrix[self.sources.index(s)]
        self.sources.remove(s)

    def _remove_receiver(self, r: Receiver):
        if r not in self.receivers:
            return

        r_target_i = self.receivers.index(r)
        for s_i in range(len(self.sources)):
            del self.sound_path_matrix[s_i][r_target_i]
        self.receivers.remove(r)

    def _remove_barrier(self, b: Barrier):
        if b not in self.barriers:
            return

        for s_i in range(len(self.sources)):
            for r_i in range(len(self.receivers)):
                try:
                    self.sound_path_matrix[s_i][r_i].allowed_barriers.remove(b)
                except KeyError:
                    continue
        self.barriers.remove(b)

    def set_directivity_loss(self, s: Source, r: Receiver, directivity_loss: float):
        sp = self.get_sr_soundpath(s, r)
        sp.directivity_loss = directivity_loss

    def set_ignore(self, s: Source, r: Receiver, ignore: bool):
        sp = self.get_sr_soundpath(s, r)
        sp.ignore = ignore

    def set_allowed_barriers(self, s: Source, r: Receiver, barriers: set[Barrier]):
        for b in barriers:
            self._add_barrier(b)
        sp = self.get_sr_soundpath(s, r)
        sp.allowed_barriers = barriers

    def get_sr_soundpath(self, s: Source, r: Receiver) -> SoundPath:
        s_i = self.sources.index(s)
        r_i = self.receivers.index(r)
        sp = self.sound_path_matrix[s_i][r_i]
        return sp


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

    def update_dBA_predictions(self, receivers: Receiver | set[Receiver] = None):
        if receivers is None:
            receivers = self.receivers
        elif isinstance(receivers, Receiver):
            receivers = {receivers}
        for r in receivers:
            self._update_dBA_predictions_helper(r)

    def _update_dBA_predictions_helper(self, r: Receiver):
        sound_paths = [self.get_sr_soundpath(s, r) for s in self.sources]
        overall_pressure = 0
        for s, sp in zip(self.sources, sound_paths):
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
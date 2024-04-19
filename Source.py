from sympy import Point
from OctaveBands import OctaveBands
from typing import Optional
from math import log10, pi


class Source:
    """A source of sound.
    Attributes:
        dBA: The dBA level of the source. If octave_band_levels are given, this is overridden.
    """

    def __init__(self,
                 geo: Point,
                 dBA: float,
                 reference_distance_ft: float,
                 octave_band_levels: Optional[OctaveBands] = None,
                 count: float = 1,
                 tag: str = None,
                 path: str = None,
                 make: str = None,
                 model: str = None,
                 q_tested: float = 2,
                 q_installed: float = 2,
                 insertion_loss: float = 0,
                ) -> None:
        self.geo = geo
        self.reference_distance_ft = abs(reference_distance_ft)
        self.octave_band_levels = octave_band_levels
        if octave_band_levels is None:
            self.dBA = dBA
        else:
            assert isinstance(self.octave_band_levels, OctaveBands)
            self.dBA = self.octave_band_levels.get_dBA()
        self.count = count
        self.tag = tag
        self.path = path
        self.make = make
        self.model = model
        self.q_tested = q_tested
        self.q_installed = q_installed
        self.insertion_loss = insertion_loss

    def set_dBA(self, dBA, reference_dist_ft=None) -> None:
        """
        Set the dBA level of the source.
        This overrides the octave band levels, setting them to zero
        """
        if reference_dist_ft is not None:
            self.reference_distance_ft = reference_dist_ft
        self.octave_band_levels = None
        self.dBA = dBA

    def set_octave_band_levels(self, octave_band_levels: OctaveBands) -> None:
        """Set the octave band levels of the source. This overrides the dBA level."""
        if not isinstance(octave_band_levels, OctaveBands):
            raise TypeError("octave_band_levels must be of type OctaveBands")
        self.octave_band_levels = octave_band_levels
        self.dBA = self.octave_band_levels.get_dBA()

    def get_LwA(self):
        if self.reference_distance_ft == 0:
            return self.dBA
        q = self.q_tested
        r = self.reference_distance_ft/3.28
        return self.dBA + 10*log10(((4 * pi * (r**2)) / q))

    def get_dBA_at_distance_ft(self, distance_ft: float):
        return self.dBA - self.get_distance_loss(distance_ft) + self.get_q_effect()
    def get_distance_loss(self, distance_ft: float):
        if self.reference_distance_ft == 0:
            q = self.q_tested
            r = distance_ft / 3.28  # distance_m
            return 10*log10((4 * pi * (r**2)) / q)
        else:
            r = self.reference_distance_ft
            return 20*log10(distance_ft / r)

    def get_q_effect(self):
        q_effect = 10*log10(self.q_installed / self.q_tested)
        return q_effect


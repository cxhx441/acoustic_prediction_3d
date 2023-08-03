from scipy import Point
import math
from random import randint
from OctaveBands import OctaveBands

class Source(Point):
    def __init__(
        self,
        point: Point,
        dBA: float,
        ref_dist: float,
        octave_band_levels: OctaveBands = None,
    ):
        super().__init__(point.x, point.y, point.z)
        self.dBA = dBA  # the dBA level of this source
        self.reference_distance = ref_dist
        self.octave_band_levels = octave_band_levels

    def set_dBA(self, dBA) -> None:
        self.octave_band_levels = None
        self.dBA = dBA

    def set_octave_band_levels(self, octave_band_levels: OctaveBands) -> None:
        if not isinstance(octave_band_levels, OctaveBands):
            raise TypeError("octave_band_levels must be of type OctaveBands")
        self.octave_band_levels = octave_band_levels
        self.dBA = self.octave_band_levels.get_dBA()

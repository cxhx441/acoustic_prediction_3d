from sympy import Point
from OctaveBands import OctaveBands

class Source():
    """ A source of sound.
        Attributes:
            dBA: The dBA level of the source. If octave_band_levels are given, this is overridden.
    """
    def __init__(
        self,
        point: Point,
        dBA: float,
        ref_dist: float,
        octave_band_levels: OctaveBands = None,
    ):
        self.point = point
        self.reference_distance = ref_dist
        self.octave_band_levels = octave_band_levels
        if octave_band_levels is None:
            self.dBA = dBA
        else:
            self.dBA = self.octave_band_levels.get_dBA()

    def set_dBA(self, dBA) -> None:
        self.octave_band_levels = None
        self.dBA = dBA

    def set_octave_band_levels(self, octave_band_levels: OctaveBands) -> None:
        if not isinstance(octave_band_levels, OctaveBands):
            raise TypeError("octave_band_levels must be of type OctaveBands")
        self.octave_band_levels = octave_band_levels
        self.dBA = self.octave_band_levels.get_dBA()

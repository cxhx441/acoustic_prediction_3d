from Geometry import Coordinate
import math
from random import randint


class OctaveBands:
    def __init__(self, hz63, hz125, hz250, hz500, hz1000, hz2000, hz4000, hz8000):
        self.hz63 = hz63
        self.hz125 = hz125
        self.hz250 = hz250
        self.hz500 = hz500
        self.hz1000 = hz1000
        self.hz2000 = hz2000
        self.hz4000 = hz4000
        self.hz8000 = hz8000

    @staticmethod
    def get_rand_ob() -> tuple[float]:
        """random octave bands for testing"""

        def rand_db():
            return randint(0, 100)

        return OctaveBands(
            rand_db(),
            rand_db(),
            rand_db(),
            rand_db(),
            rand_db(),
            rand_db(),
            rand_db(),
            rand_db(),
        )

    def get_OB_sound_levels(self) -> tuple[float]:
        return (
            self.hz63,
            self.hz125,
            self.hz250,
            self.hz500,
            self.hz1000,
            self.hz2000,
            self.hz4000,
            self.hz8000,
        )

    def get_OB_A_weigthed_sound_levels(self) -> tuple[float]:
        ob_a_weighting_list = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
        return (x + y for x, y in zip(self.get_OB_sound_levels(), ob_a_weighting_list))

    def get_dBA(self) -> float:
        # return acoustics.decibel.dbadd(self.get_OB_A_weigthed_sound_levels(), [])
        dBA = 0
        for lvl in self.get_OB_A_weigthed_sound_levels():
            dBA += 10 ** (lvl / 10)
        return 10 * math.log10(dBA)

    def __str__(self):
        return str(self.get_OB_sound_levels())


class Source(Coordinate):
    def __init__(
        self,
        coords: Coordinate,
        dBA: float,
        ref_dist: float,
        octave_band_levels: OctaveBands = None,
    ):
        super().__init__(coords.x, coords.y, coords.z)
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

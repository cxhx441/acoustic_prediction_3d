from Geometry import Point
import acoustics.decibel
import math


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

    def get_OB_sound_levels(self):
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

    def get_OB_A_weigthed_sound_levels(self):
        ob_a_weighting_list = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
        return (x + y for x, y in zip(self.get_OB_sound_levels(), ob_a_weighting_list))

    def get_dBA(self):
        # return acoustics.decibel.dbadd(self.get_OB_A_weigthed_sound_levels(), [])
        dBA = 0
        for lvl in self.get_OB_A_weigthed_sound_levels():
            dBA += 10 ** (lvl / 10)
        return 10 * math.log10(dBA)


class Source(Point):
    def __init__(
        self,
        coords: Point,
        dBA: float,
        ref_dist: float,
        ob_sound_levels: OctaveBands = None,
    ):
        super().__init__(coords.x, coords.y, coords.z)
        self.dBA = dBA  # the dBA level of this source
        self.reference_distance = ref_dist
        self.ob_sound_levels = ob_sound_levels

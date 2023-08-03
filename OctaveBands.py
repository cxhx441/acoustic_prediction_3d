from random import randint
from math import log10
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
    def get_static_ob(ob_db=100) -> tuple[float]:
        """
        random octave bands for testing
        lower and upper are the bounds for the random ob values. default is 0 to 100
        """

        return OctaveBands(
            ob_db,
            ob_db,
            ob_db,
            ob_db,
            ob_db,
            ob_db,
            ob_db,
            ob_db,
        )

    @staticmethod
    def get_rand_ob(lower=0, upper=100) -> tuple[float]:
        """
        random octave bands for testing
        lower and upper are the bounds for the random ob values. default is 0 to 100
        """

        def rand_db():
            return randint(lower, upper)

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
        return 10 * log10(dBA)

    def __str__(self):
        return str(self.get_OB_sound_levels())
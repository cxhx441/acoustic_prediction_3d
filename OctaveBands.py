from random import randint
from math import log10


class OctaveBands:
    def __init__(self, octave_bands: tuple[float]) -> None:
        """
        octave_bands must be an iterable of 8 floats corresponding to
            center frequencies octave bands 63 to 8kHz
        """
        self.octave_bands = {
            63: octave_bands[0],
            125: octave_bands[1],
            250: octave_bands[2],
            500: octave_bands[3],
            1000: octave_bands[4],
            2000: octave_bands[5],
            4000: octave_bands[6],
            8000: octave_bands[7],
        }

    @staticmethod
    def get_static_ob(ob_db=100) -> tuple[float]:
        """
        random octave bands for testing
        lower and upper are the bounds for the random ob values. default is 0 to 100
        """
        return OctaveBands([ob_db] * 8)

    @staticmethod
    def get_rand_ob(lower=0, upper=100) -> tuple[float]:
        """
        random octave bands for testing
        lower and upper are the bounds for the random ob values. default is 0 to 100
        """

        def rand_db():
            return randint(lower, upper)

        return OctaveBands([rand_db() for _ in range(8)])

    def get_OB_sound_levels(self) -> tuple[float]:
        return tuple(self.octave_bands.values())

    def get_OB_A_weigthed_sound_levels(self) -> list[float]:
        ob_a_weighting_list = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
        return [x + y for x, y in zip(self.get_OB_sound_levels(), ob_a_weighting_list)]

    def get_dBA(self) -> float:
        # return acoustics.decibel.dbadd(self.get_OB_A_weigthed_sound_levels(), [])
        dBA = 0
        for lvl in self.get_OB_A_weigthed_sound_levels():
            dBA += 10 ** (lvl / 10)
        return 10 * log10(dBA)

    # def __str__(self):
    #     return str(self.get_OB_sound_levels())

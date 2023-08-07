from random import randint
from math import log10
from functools import reduce


class OctaveBands:
    OB_A_WEIGHTING_LIST = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]

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
        return OctaveBands([randint(lower, upper) for _ in range(8)])

    def get_OB_sound_levels(self) -> tuple[float]:
        """Return the octave bands as a tuple"""
        return tuple(self.octave_bands.values())

    def get_OB_A_weigthed_sound_levels(self) -> list[float]:
        """Return the A-weighted octave bands"""
        return [
            x + y
            for x, y in zip(self.get_OB_sound_levels(), OctaveBands.OB_A_WEIGHTING_LIST)
        ]

    def get_dBA(self) -> float:
        """Return the dBA level of the octave bands"""
        pressure = 0
        for lvl in self.get_OB_A_weigthed_sound_levels():
            pressure += 10 ** (lvl / 10)
        return 10 * log10(pressure)

    # def __str__(self):
    #     return str(self.get_OB_sound_levels())

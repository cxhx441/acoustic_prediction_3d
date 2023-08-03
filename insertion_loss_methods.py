import math
from Source import Source  # for type hinting
import operator
from acoustics.decibel import dbsum

def ARI_interpolation(pld, lowerIL, upperIL, lowerPLD, upperPLD):
    diff_in_reduction = (pld - lowerPLD) / (upperPLD - lowerPLD)
    change_IL = upperIL - lowerIL
    barrier_IL = lowerIL + change_IL * diff_in_reduction
    return int(round(barrier_IL, 0))


def get_ARI_il(pld: float):

    # TODO Flip this to start at if pld > 12, elif pld > 6, etc. Although, this is not a big deal and this is clearer.
    if 0 < pld and pld <= 0.5:
        barrier_IL = ARI_interpolation(pld, 0, 4, 0, 0.5)
    elif 0.5 < pld and pld <= 1:
        barrier_IL = ARI_interpolation(pld, 4, 7, 0.5, 1)
    elif 1 < pld and pld <= 2:
        barrier_IL = ARI_interpolation(pld, 7, 10, 1, 2)
    elif 2 < pld and pld <= 3:
        barrier_IL = ARI_interpolation(pld, 10, 12, 2, 3)
    elif 3 < pld and pld <= 6:
        barrier_IL = ARI_interpolation(pld, 12, 15, 3, 6)
    elif 6 < pld and pld <= 12:
        barrier_IL = ARI_interpolation(pld, 15, 17, 6, 12)
    elif 12 < pld:
        barrier_IL = 17
    else:
        barrier_IL = 0

    return barrier_IL


def get_fresnel_numbers(pld, c):
    """
    pld = path length difference
    c = speed of sound
    """
    ob_frequencies = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
    return [(2 * pld) / (c / ob) for ob in ob_frequencies]


def get_fresnel_il(s: Source, pld: float) -> float:
    a_weights = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
    eqmt_lvl = s.dBA
    ob_levels = list(s.octave_band_levels.get_OB_sound_levels())
    speed_of_sound = 1128
    fresnel_num_list = get_fresnel_numbers(pld, speed_of_sound)
    ob_barrier_attenuation = get_ob_barrier_attenuation(fresnel_num_list)
    ob_levels = map(operator.sub, ob_levels, ob_barrier_attenuation)
    ob_levels = map(operator.add, ob_levels, a_weights)

    attenuated_aweighted_level = dbsum(ob_levels)

    barrier_IL = eqmt_lvl - attenuated_aweighted_level


def get_ob_barrier_attenuation(fresnel_nums):
    line_point_correction = 0  # assume point source (0=point, -5=line).
    barrier_finite_infinite_correction = (
        1.0  # assume infinite barrier see Mehta for correction under finite barrier.
    )
    Kb_barrier_constant = 5  # assume Kb (barrier const.) for wall=5, berm=8
    barrier_attenuate_limit = 20  # wall limit = 20 berm limit = 23

    ob_barrier_attenuation_list = []
    for N in fresnel_nums:
        n_d = math.sqrt(2 * math.pi * N)
        ob_barrier_attenuation = (
            (20 * math.log10(n_d / math.tanh(n_d)))
            + Kb_barrier_constant
            + line_point_correction
        ) ** barrier_finite_infinite_correction

        if ob_barrier_attenuation > barrier_attenuate_limit:
            ob_barrier_attenuation = barrier_attenuate_limit
        ob_barrier_attenuation_list.append(ob_barrier_attenuation)

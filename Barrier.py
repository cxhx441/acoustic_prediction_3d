from Geometry import Line, Coordinate
from Source import Source  # for type hinting
from Receiver import Receiver  # for type hinting
import utils  # refactor to not need this.
import math
import acoustics.decibel


class Barrier(Line):
    def __init__(
        self,
        start_coords: Coordinate,
        end_coords: Coordinate,
    ) -> None:
        super().__init__(start_coords, end_coords)

    def ARI_il(self, path_length_difference):
        pld = path_length_difference

        def ARI_interpolation(pld, lowerIL, upperIL, lowerPLD, upperPLD):
            diff_in_reduction = (pld - lowerPLD) / (upperPLD - lowerPLD)
            change_IL = upperIL - lowerIL
            barrier_IL = lowerIL + change_IL * diff_in_reduction
            return int(round(barrier_IL, 0))

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

    def get_insertion_loss_ARI(self, s: Source, r: Receiver) -> float:
        """TODO refactor me"""
        eqmt_x, eqmt_y, eqmt_z = s.get_coords()
        bar_x0, bar_y0, bar_z0 = self.get_start_coords()
        bar_x1, bar_y1, bar_z1 = self.get_end_coords()
        rcvr_x, rcvr_y, rcvr_z = r.get_coords()

        # fixing escape on error with same barrier coordinate
        if bar_x0 == bar_x1:
            bar_x0 += 0.0001
            print("corrected bar_x0==bar_x1 error")
        if bar_y0 == bar_y1:
            bar_y0 += 0.0001
            print("corrected bar_y0==bar_y1 error")
        # testing if line of sight is broken along HORIZONTAL plane
        eqmt_point = utils.Point(eqmt_x, eqmt_y)
        receiver_point = utils.Point(rcvr_x, rcvr_y)
        bar_start_point = utils.Point(bar_x0, bar_y0)
        bar_end_point = utils.Point(bar_x1, bar_y1)
        if not utils.doIntersect(
            eqmt_point, receiver_point, bar_start_point, bar_end_point
        ):
            print("barrier fails horizontal test")
            return 0

        try:
            m_source2receiver = (rcvr_y - eqmt_y) / (rcvr_x - eqmt_x)
        except ZeroDivisionError:
            return 0
        try:
            m_bar_start2end = (bar_y0 - bar_y1) / (bar_x0 - bar_x1)
        except ZeroDivisionError:
            return 0

        b_source2receiver = eqmt_y - (eqmt_x * m_source2receiver)
        b_bar_start2end = bar_y0 - (bar_x0 * m_bar_start2end)
        intersection_x = (b_bar_start2end - b_source2receiver) / (
            m_source2receiver - m_bar_start2end
        )
        intersection_y = m_source2receiver * intersection_x + b_source2receiver

        bar_min_z = min(bar_z0, bar_z1)
        bar_height_difference = abs(bar_z0 - bar_z1)
        bar_length = utils.distance_formula(x0=bar_x0, y0=bar_y0, x1=bar_x1, y1=bar_y1)
        bar_slope = bar_height_difference / bar_length
        if bar_z0 <= bar_z1:
            bar_dist2barxpoint = utils.distance_formula(
                x0=intersection_x, y0=intersection_y, x1=bar_x0, y1=bar_y0
            )
        else:
            bar_dist2barxpoint = utils.distance_formula(
                x0=intersection_x, y0=intersection_y, x1=bar_x1, y1=bar_y1
            )

        bar_height_to_use = bar_slope * bar_dist2barxpoint + bar_min_z

        # testing if line of sight is broken vertically
        if bar_height_to_use < eqmt_z and bar_height_to_use < rcvr_z:
            print("barrier fails easy vertical test")
            return 0

        distance_source2receiver_horizontal = utils.distance_formula(
            x0=eqmt_x, y0=eqmt_y, x1=rcvr_x, y1=rcvr_y
        )
        distance_source2bar_horizontal = utils.distance_formula(
            x0=eqmt_x, y0=eqmt_y, x1=intersection_x, y1=intersection_y
        )
        distance_barrier2receiever_straight = (
            distance_source2receiver_horizontal - distance_source2bar_horizontal
        )
        distance_source2receiver_propogation = math.sqrt(
            distance_source2receiver_horizontal**2 + (rcvr_z - eqmt_z) ** 2
        )
        distance_source2barrier_top = math.sqrt(
            (bar_height_to_use - eqmt_z) ** 2 + distance_source2bar_horizontal**2
        )
        distance_receiver2barrier_top = math.sqrt(
            (bar_height_to_use - rcvr_z) ** 2 + distance_barrier2receiever_straight**2
        )
        path_length_difference = (
            distance_source2barrier_top
            + distance_receiver2barrier_top
            - distance_source2receiver_propogation
        )

        # testing if line of sight is broken along VERTICAL plane
        eqmt_point = utils.Point(0, eqmt_z)
        receiver_point = utils.Point(distance_source2receiver_horizontal, rcvr_z)
        bar_start_point = utils.Point(distance_source2bar_horizontal, 0)
        bar_end_point = utils.Point(distance_source2bar_horizontal, bar_height_to_use)
        if not utils.doIntersect(
            eqmt_point, receiver_point, bar_start_point, bar_end_point
        ):
            print("barrier fails vertical test")
            return 0

        pld = path_length_difference
        barrier_IL = self.ARI_il(pld)

        return [
            barrier_IL,
            bar_height_to_use,
            distance_source2receiver_horizontal,
            distance_source2bar_horizontal,
            distance_source2barrier_top,
            distance_receiver2barrier_top,
            distance_source2receiver_propogation,
            path_length_difference,
            "ARI",
        ]

    def get_insertion_loss_OB_fresnel(self, s: Source, r: Receiver) -> float:
        """TODO refactor me"""
        eqmt_x, eqmt_y, eqmt_z = s.get_coords()
        bar_x0, bar_y0, bar_z0 = self.get_start_coords()
        bar_x1, bar_y1, bar_z1 = self.get_end_coords()
        rcvr_x, rcvr_y, rcvr_z = r.get_coords()
        (
            hz63,
            hz125,
            hz250,
            hz500,
            hz1000,
            hz2000,
            hz4000,
            hz8000,
        ) = s.ob_sound_levels.get_OB_sound_levels()
        eqmt_level = s.dBA

        # fixing escape on error with same barrier coordinate
        if bar_x0 == bar_x1:
            bar_x0 += 0.0001
            print("corrected bar_x0==bar_x1 error")
        if bar_y0 == bar_y1:
            bar_y0 += 0.0001
            print("corrected bar_y0==bar_y1 error")
        ob_levels_list = [hz63, hz125, hz250, hz500, hz1000, hz2000, hz4000, hz8000]
        ob_bands_list = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        # testing if line of sight is broken along horizontal plane
        eqmt_point = utils.Point(eqmt_x, eqmt_y)
        receiver_point = utils.Point(rcvr_x, rcvr_y)
        bar_start_point = utils.Point(bar_x0, bar_y0)
        bar_end_point = utils.Point(bar_x1, bar_y1)
        if not utils.doIntersect(
            eqmt_point, receiver_point, bar_start_point, bar_end_point
        ):
            print("barrier fails horizontal test")
            return 0
        try:
            m_source2receiver = (rcvr_y - eqmt_y) / (rcvr_x - eqmt_x)
        except ZeroDivisionError:
            return 0
        try:
            m_bar_start2end = (bar_y0 - bar_y1) / (bar_x0 - bar_x1)
        except ZeroDivisionError:
            return 0

        b_source2receiver = eqmt_y - (eqmt_x * m_source2receiver)
        b_bar_start2end = bar_y0 - (bar_x0 * m_bar_start2end)
        intersection_x = (b_bar_start2end - b_source2receiver) / (
            m_source2receiver - m_bar_start2end
        )
        intersection_y = m_source2receiver * intersection_x + b_source2receiver

        bar_min_z = min(bar_z0, bar_z1)
        bar_height_difference = abs(bar_z0 - bar_z1)
        bar_length = utils.distance_formula(x0=bar_x0, y0=bar_y0, x1=bar_x1, y1=bar_y1)
        bar_slope = bar_height_difference / bar_length
        if bar_z0 <= bar_z1:
            bar_dist2barxpoint = utils.distance_formula(
                x0=intersection_x, y0=intersection_y, x1=bar_x0, y1=bar_y0
            )
        else:
            bar_dist2barxpoint = utils.distance_formula(
                x0=intersection_x, y0=intersection_y, x1=bar_x1, y1=bar_y1
            )

        bar_height_to_use = bar_slope * bar_dist2barxpoint + bar_min_z

        # testing if line of sight is broken vertically
        if bar_height_to_use < eqmt_z and bar_height_to_use < rcvr_z:
            print("barrier fails easy vertical test")
            return 0

        distance_source2receiver_horizontal = utils.distance_formula(
            x0=eqmt_x, y0=eqmt_y, x1=rcvr_x, y1=rcvr_y
        )
        distance_source2bar_horizontal = utils.distance_formula(
            x0=eqmt_x, y0=eqmt_y, x1=intersection_x, y1=intersection_y
        )
        distance_barrier2receiever_straight = (
            distance_source2receiver_horizontal - distance_source2bar_horizontal
        )
        distance_source2receiver_propogation = math.sqrt(
            distance_source2receiver_horizontal**2 + (rcvr_z - eqmt_z) ** 2
        )
        distance_source2barrier_top = math.sqrt(
            (bar_height_to_use - eqmt_z) ** 2 + distance_source2bar_horizontal**2
        )
        distance_receiver2barrier_top = math.sqrt(
            (bar_height_to_use - rcvr_z) ** 2 + distance_barrier2receiever_straight**2
        )
        path_length_difference = (
            distance_source2barrier_top
            + distance_receiver2barrier_top
            - distance_source2receiver_propogation
        )

        # testing if line of sight is broken along VERTICAL plane
        eqmt_point = utils.Point(0, eqmt_z)
        receiver_point = utils.Point(distance_source2receiver_horizontal, rcvr_z)
        bar_start_point = utils.Point(distance_source2bar_horizontal, 0)
        bar_end_point = utils.Point(distance_source2bar_horizontal, bar_height_to_use)
        if not utils.doIntersect(
            eqmt_point, receiver_point, bar_start_point, bar_end_point
        ):
            print("barrier fails vertical test")
            return 0

        speed_of_sound = 1128
        fresnel_num_list = [
            (2 * path_length_difference) / (speed_of_sound / ob) for ob in ob_bands_list
        ]

        line_point_correction = (
            0  # assume no line/point source correction 0 for point, -5 for line
        )
        barrier_finite_infinite_correction = 1.0  # assume infinite barrier see Mehta for correction under finite barrier.
        Kb_barrier_constant = 5  # assume Kb (barrier constant) for wall = 5, berm = 8
        barrier_attenuate_limit = 20  # wall limit = 20 berm limit = 23

        ob_barrier_attenuation_list = []
        for N in fresnel_num_list:
            n_d = math.sqrt(2 * math.pi * N)
            ob_barrier_attenuation = (
                (20 * math.log10(n_d / math.tanh(n_d)))
                + Kb_barrier_constant
                + line_point_correction
            ) ** barrier_finite_infinite_correction

            if ob_barrier_attenuation > barrier_attenuate_limit:
                ob_barrier_attenuation = barrier_attenuate_limit
            ob_barrier_attenuation_list.append(ob_barrier_attenuation)

        ob_attenuated_levels_list = [
            x - y for x, y in zip(ob_levels_list, ob_barrier_attenuation_list)
        ]
        ob_a_weighting_list = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
        ob_attenuated_aweighted_levels_list = [
            x + y for x, y in zip(ob_attenuated_levels_list, ob_a_weighting_list)
        ]

        attenuated_aweighted_level = acoustics.decibel.dbsum(
            ob_attenuated_aweighted_levels_list
        )

        barrier_IL = eqmt_level - attenuated_aweighted_level

        return [
            round(barrier_IL, 1),
            bar_height_to_use,
            distance_source2receiver_horizontal,
            distance_source2bar_horizontal,
            distance_source2barrier_top,
            distance_receiver2barrier_top,
            distance_source2receiver_propogation,
            path_length_difference,
            "OB-Fresnel",
        ]

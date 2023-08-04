from sympy import Point, Line, Segment, Ray
from Source import Source  # TODO just for type hint
from Receiver import Receiver  # TODO just for type hint
from Barrier import Barrier  # TODO just for type hint
import operator
from acoustics.decibel import dbsum
import math

DEBUG = True


def log(*args):
    if DEBUG:
        print(*args)


class InsertionLoss:
    def __init__(self, barrier: Barrier, source: Source, receiver: Receiver):
        self.b = barrier
        self.s = source
        self.r = receiver

        self.s_r = Segment(self.s, self.r)
        # self.update_horizontal_section_attr()
        self.horizontal_section = HorizontalSection(self.b, self.s, self.r)
        self.bar_cross_point_3D = self.get_barrier_cross_point_3D_attr()
        # self.update_vertical_section_attr()
        self.vertical_section = VerticalSection(self.b, self.s, self.r)
        self.pld = self.get_pld()
        self.il_ari = self.get_ARI_il()
        self.il_fresnel = self.get_fresnel_il()

    def get_attr_for_graph(self):
        dist_source2receiver_horizontal = self.horiz_2D_s.distance(self.horiz_2D_r)
        dist_source2bar_horizontal = self.horiz_2D_s.distance(self.horiz_2D_intersect)
        dist_source2receiver_propogation = self.s_r.length
        dist_source2barrier_top = self.s.distance(self.bar_cross_point_3D)
        dist_receiver2barrier_top = self.r.distance(self.bar_cross_point_3D)
        pld = (
            dist_source2barrier_top
            + dist_receiver2barrier_top
            - dist_source2receiver_propogation
        )

        return [
            round(self.bar_cross_point_3D.z, 2),
            round(dist_source2receiver_horizontal, 2),
            round(dist_source2bar_horizontal, 2),
            round(dist_source2barrier_top, 2),
            round(dist_receiver2barrier_top, 2),
            round(dist_source2receiver_propogation, 2),
            round(pld, 2),
        ]

    def get_pld(self):
        # this section is legacy... hope to delete
        dist_source2receiver_horizontal = self.horiz_2D_s.distance(self.horiz_2D_r)
        dist_source2bar_horizontal = self.horiz_2D_s.distance(self.horiz_2D_intersect)
        dist_source2receiver_propogation = self.s_r.length
        dist_source2barrier_top = self.s.distance(self.bar_cross_point_3D)
        dist_receiver2barrier_top = self.r.distance(self.bar_cross_point_3D)
        pld_1 = (
            dist_source2barrier_top
            + dist_receiver2barrier_top
            - dist_source2receiver_propogation
        )
        # end legacy section

        pld_2 = (
            self.s.distance(self.bar_cross_point_3D)
            + self.r.distance(self.bar_cross_point_3D)
            - self.s.dicstance(self.r)
        )

        if pld_1 != pld_2:
            log("pld_1 != pld_2")
            raise Exception("pld_1 != pld_2")

        return pld_2

    def get_vertical_intersect(self, s: Source, r: Receiver):
        intersect = self.vert_2D_s_r_segment.intersection(self.vert_2D_bar_ray)

        if intersect == []:
            log("barrier fails VERTICAL test")
            return None
        else:
            return intersect[0]

    def segment_is_grazing_other(self) -> bool:
        """returns True if either the start or end point of the source-receiver line lie on the barrier line, or vice versa"""
        l1 = self.horiz_2D_s_r_segment
        l2 = self.horiz_2D_bar_segment

        return (
            l1.contains(l2.p1)
            or l1.contains(l2.p2)
            or l2.contains(l1.p1)
            or l2.contains(l1.p2)
        )

    def get_barrier_cross_point_3D_attr(self):
        vert_3Dline_at_intersect = Line(
            self.horiz_2D_intersect, self.horiz_2D_intersect + Point(0, 0, 1)
        )
        bar_cross_3Dpoint = vert_3Dline_at_intersect.intersection(self)[0]
        s_r_cross_3Dpoint = vert_3Dline_at_intersect.intersection(self.s_r)[0]

        # testing if line of sight is broken vertically
        if s_r_cross_3Dpoint.z < bar_cross_3Dpoint.z:
            raise Exception("barrier fails EASY vertical test")

        return Point(
            self.horiz_2D_intersect.x, self.horiz_2D_intersect.y, bar_cross_3Dpoint.z
        )

    @staticmethod
    def get_fresnel_numbers(self, pld, c):
        """
        pld = path length difference
        c = speed of sound
        """
        ob_frequencies = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        return [(2 * pld) / (c / ob) for ob in ob_frequencies]

    @staticmethod
    def get_ob_bar_attenuation(fresnel_nums):
        line_point_correction = 0  # assume point source (0=point, -5=line).
        # assume infinite barrier see Mehta for correction under finite barrier.
        barrier_finite_infinite_correction = 1.0
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

    def get_fresnel_il(self) -> float:
        a_weights = [-26.2, -16.1, -8.6, -3.2, -0, 1.2, 1, -1.1]
        eqmt_lvl = self.s.dBA
        ob_levels = list(self.s.octave_band_levels.get_OB_sound_levels())
        speed_of_sound = 1128
        fresnel_num_list = InsertionLoss.get_fresnel_numbers(self.pld, speed_of_sound)
        ob_bar_attenuation = InsertionLoss.get_ob_bar_attenuation(fresnel_num_list)
        ob_levels = map(operator.sub, ob_levels, ob_bar_attenuation)
        ob_levels = map(operator.add, ob_levels, a_weights)

        attenuated_aweighted_level = dbsum(ob_levels)

        barrier_IL = eqmt_lvl - attenuated_aweighted_level

        return barrier_IL

    @staticmethod
    def ARI_interpolation(pld, lowerIL, upperIL, lowerPLD, upperPLD):
        diff_in_reduction = (pld - lowerPLD) / (upperPLD - lowerPLD)
        change_IL = upperIL - lowerIL
        barrier_IL = lowerIL + change_IL * diff_in_reduction
        return int(round(barrier_IL, 0))

    def get_ARI_il(self):
        # TODO Flip this to start at if pld > 12, elif pld > 6, etc. Although, this is not a big deal and this is clearer.
        pld = self.pld
        if 0 < pld and pld <= 0.5:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 0, 4, 0, 0.5)
        elif 0.5 < pld and pld <= 1:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 4, 7, 0.5, 1)
        elif 1 < pld and pld <= 2:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 7, 10, 1, 2)
        elif 2 < pld and pld <= 3:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 10, 12, 2, 3)
        elif 3 < pld and pld <= 6:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 12, 15, 3, 6)
        elif 6 < pld and pld <= 12:
            barrier_IL = InsertionLoss.ARI_interpolation(pld, 15, 17, 6, 12)
        elif 12 < pld:
            barrier_IL = 17
        else:
            barrier_IL = 0

        return barrier_IL


class HorizontalSection:
    def __init__(self, barrier: Barrier, source: Source, receiver: Receiver):
        self.s = Point(source.x, source.y, 0)
        self.r = Point(receiver.x, receiver.y, 0)
        self.s_r = Segment(self.s, self.r)
        self.bar_p1 = Point(barrier.p1.x, barrier.p1.y, 0)
        self.bar_p2 = Point(barrier.p2.x, barrier.p2.y, 0)
        self.bar = Segment(self.bar_p1, self.bar_p2)
        try:
            self.intersect = self.s_r.intersection(self.bar)[0]
        except IndexError:
            self.intersect = None


class VerticalSection:
    def __init__(
        self,
        source: Source,
        receiver: Receiver,
        bar_cross_point_3D: Point,
        h_sect: HorizontalSection,
    ):
        self.s = Point(0, source.z, 0)
        self.r = Point(h_sect.s.distance(h_sect.r), receiver.z, 0)
        self.s_r = Segment(self.s, self.r)
        self.bar_cross_point = Point(
            self.h_sect.s.distance(h_sect.intersect),
            bar_cross_point_3D.z,
            0,
        )
        self.bar = Ray(self.bar_cross_point, self.bar_cross_point + Point(0, -1, 0))

        try:
            self.intersect = self.s_r.intersection(self.bar)[0]
        except IndexError:
            self.intersect = None

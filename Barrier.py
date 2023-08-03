from Source import Source  # for type hinting
from Receiver import Receiver  # for type hinting
import utils  # refactor to not need this.
from sympy import Line, Point, Segment, Ray
import math
from acoustics.decibel import dbsum
import operator
import insertion_loss_methods as il_methods

DEBUG = True


def log(*args):
    if DEBUG:
        print(*args)


class Barrier(Segment):
    def __init__(self, *args) -> None:
        if len(args) == 1:
            try:
                super().__init__(args[0].p1, args[0].p2)
            except AttributeError:
                raise TypeError("args must be 2 Point objects or 1 Line object")

        elif len(args) == 2:
            try:
                super().__init__(args[0], args[1])
            except AttributeError:
                raise TypeError("args must be 2 Point objects or 1 Line object")

    def line_vertex_lie_on_other_line(self, s: Source, r: Receiver) -> bool:
        s_2D = Point(s.x, s.y, 0)
        r_2D = Point(r.x, r.y, 0)
        bar_p1_2D = Point(self.p1.x, self.p1.y, 0)
        bar_p2_2D = Point(self.p2.x, self.p2.y, 0)
        s_r_segment_2D = Segment(s_2D, r_2D)
        bar_segment_2D = Segment(bar_p1_2D, bar_p2_2D)

        return (
            s_r_segment_2D.contains(bar_p1_2D)
            or s_r_segment_2D.contains(bar_p2_2D)
            or bar_segment_2D.contains(s_2D)
            or bar_segment_2D.contains(r_2D)
        )

    def get_horizontal_intersection(self, s: Source, r: Receiver):
        s_2D = Point(s.x, s.y, 0)
        r_2D = Point(r.x, r.y, 0)
        bar_p1_2D = Point(self.p1.x, self.p1.y, 0)
        bar_p2_2D = Point(self.p2.x, self.p2.y, 0)
        s_r_segment_2D = Segment(s_2D, r_2D)
        bar_segment_2D = Segment(bar_p1_2D, bar_p2_2D)
        intersection = s_r_segment_2D.intersection(bar_segment_2D)

        if intersection == []:
            log("barrier fails HORIZONTAL test")
            return None
        else:
            return intersection[0]

    def get_vertical_intersection(self, s: Source, r: Receiver):
        s_2D = Point(s.x, s.z, 0)
        r_2D = Point(r.x, r.z, 0)
        s_r_segment_2D = Segment(s_2D, r_2D)

        bar_z = max(self.p1.z, self.p2.z)
        bar_p1_2D = Point(self.p1.x, bar_z, 0)
        bar_ray_2D = Ray(bar_p1_2D, bar_p1_2D + Point(0, -1, 0))

        intersection = s_r_segment_2D.intersection(bar_ray_2D)

        if intersection == []:
            log("barrier fails VERTICAL test")
            return None
        else:
            return intersection[0]

    def get_barrier_cross_point_3D(self, horizontal_intersect, s_r_segment_3D):
        vertical_3Dline_at_intersect = Line(
            horizontal_intersect, horizontal_intersect + Point(0, 0, 1)
        )
        bar_cross_point_3D = vertical_3Dline_at_intersect.intersection(self)[0]
        s_r_cross_point_3D = vertical_3Dline_at_intersect.intersection(s_r_segment_3D)[
            0
        ]

        # testing if line of sight is broken vertically
        if s_r_cross_point_3D.z < bar_cross_point_3D.z:
            raise Exception("barrier fails EASY vertical test")

        return Point(
            horizontal_intersect.x, horizontal_intersect.y, bar_cross_point_3D.z
        )

    def get_insertion_loss(self, s: Source, r: Receiver, method: str) -> float:
        """TODO refactor me"""

        if method not in ("ARI", "Fresnel"):
            raise Exception("method must be ARI or Fresnel")

        s_r_segment_3D = Segment(s, r)
        s_2D = Point(s.x, s.y, 0)
        r_2D = Point(r.x, r.y, 0)

        if Barrier.line_vertex_lie_on_other_line(self, s, r):
            log("start or end point is on other line entity")
            return 0

        # if bar_segment_2D.is_parallel(s_r_segment_2D):
        #     raise Exception("barrier is parallel to source-receiver line")
        #     # return 0

        # testing if line of sight is broken along horizontal/vertical planeh
        if Barrier.get_vertical_intersection(self, s, r) is None:
            return 0

        horizontal_intersect = Barrier.get_horizontal_intersection(self, s, r)
        if horizontal_intersect is None:
            return 0

        # getting height of barrier at intersection point
        try:
            bar_cross_point_3D = self.get_barrier_cross_point_3D(
                horizontal_intersect, s_r_segment_3D
            )
        except Exception as e:
            print(e)
            return 0

        dist_source2receiver_horizontal = s_2D.distance(r_2D)
        dist_source2bar_horizontal = s_2D.distance(horizontal_intersect)
        dist_source2receiver_propogation = s_r_segment_3D.length
        dist_source2barrier_top = s.distance(bar_cross_point_3D)
        dist_receiver2barrier_top = r.distance(bar_cross_point_3D)
        pld = (
            dist_source2barrier_top
            + dist_receiver2barrier_top
            - dist_source2receiver_propogation
        )

        if pld <= 0:
            raise Exception("PLD <= 0")
            # return 0

        ret_list = [
            round(bar_cross_point_3D.z, 2),
            round(dist_source2receiver_horizontal, 2),
            round(dist_source2bar_horizontal, 2),
            round(dist_source2barrier_top, 2),
            round(dist_receiver2barrier_top, 2),
            round(dist_source2receiver_propogation, 2),
            round(pld, 2),
        ]

        if method == "ARI":
            pld = pld
            barrier_IL = il_methods.get_ARI_il(pld)
            return [barrier_IL] + ret_list + ["ARI"]

        elif method == "Fresnel" and s.octave_band_levels is not None:
            barrier_IL = il_methods.get_fresnel_il(s)
            return [barrier_IL] + ret_list + ["OB-Fresnel"]

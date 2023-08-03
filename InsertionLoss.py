from sympy import Point, Line, Segment, Ray
from Source import Source  # TODO just for type hint
from Receiver import Receiver  # TODO just for type hint
from Barrier import Barrier  # TODO just for type hint
import insertion_loss_methods as il_methods


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
        barrier: Barrier,
        source: Source,
        receiver: Receiver,
        bar_cross_point_3D: Point,
        h_sect: HorizontalSection,
    ):
        self.s = Point(0, source.z, 0)
        self.r = Point(h_sect.s.distance(h_sect.r), receiver.z, 0)
        self.s_r = Segment(self.s, self.r)
        self.bar_cross_point = Point( self.h_sect.s.distance(h_sect.intersect), bar_cross_point_3D.z, 0,)
        self.bar = Ray(self.bar_cross_point, self.bar_cross_point + Point(0, -1, 0))

        try:
            self.intersect = self.s_r.intersection(self.bar)[0]
        except IndexError:
            self.intersect = None


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
        self.update_pld()
        self.update_insertion_loses()

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

    def update_pld(self):
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
            raise Exception("pld_1 != pld_2")

        self.pld = pld_2

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

    def update_insertion_losses(self) -> float:
        """TODO refactor me"""

        # if self.segment_is_grazing_other(self):
        #     log("start or end point is on other line entity")
        #     return 0

        # if bar_segment_2D.is_parallel(s_r_segment_2D):
        #     raise Exception("barrier is parallel to source-receiver line")
        #     # return 0

        # testing if line of sight is broken along horizontal/vertical planeh
        if (
            self.segment_is_grazing_other()
            or self.horiz_2D_intersect is None
            or self.vert_2D_intersect is None
            or self.bar_cross_point_3D is None
            or self.pld == 0
        ):
            return 0

        self.insertion_loss_ARI = il_methods.get_ARI_il(self.pld)
        self.insertion_loss_FRESNEL = il_methods.get_fresnel_il(self.s, self.pld)

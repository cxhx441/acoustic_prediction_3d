from scipy import Point, Line, Segment, Ray
from Source import Source  # TODO just for type hint
from Receiver import Receiver  # TODO just for type hint
from Barrier import Barrier  # TODO just for type hint
import insertion_loss_methods as il_methods


class InsertionLoss:
    def __init__(self, barrier: Barrier, source: Source, receiver: Receiver):
        self.b = barrier
        self.s = source
        self.r = receiver

        self.s_r = Segment(self.s, self.r)
        self.update_horizontal_section_attr()
        self.update_barrier_cross_point_3D_attr()
        self.update_vertical_section_attr()
        self.update_pld()
        self.update_insertion_loses()

    # for 2D horizontal plane calculations
    def update_horizontal_section_attr(self):
        """used in initialization and update methods"""
        self.horiz_2D_s = (Point(self.s.x, self.s.y, 0),)
        self.horiz_2D_r = (Point(self.r.x, self.r.y, 0),)
        self.horiz_2D_s_r_segment = Segment(self.horiz_2D_s, self.horiz_2D_r)
        self.horiz_2D_bar_p1 = (Point(self.b.p1.x, self.b.p1.y, 0),)
        self.horiz_2D_bar_p2 = (Point(self.b.p2.x, self.b.p2.y, 0),)
        self.horiz_2D_bar_segment = Segment(self.horiz_2D_bar_p1, self.horiz_2D_bar_p2)
        try:
            self.horiz_2D_intersect = self.horiz_2D_s_r_segment.intersection(
                self.horiz_2D_bar_segment
            )[0]
        except IndexError:
            self.horiz_2D_intersect = None

    # TODO this is actuall wrong as it doesn't take into account the actuall distances between the elements
    # TODO do we need this with the other vertical check?
    # for 2D vertical plane calculations
    def update_vertical_section_attr(self):
        """
        used in initialization and update methods
        """

        self.vert_2D_s = Point(0, self.s.z, 0)
        self.vert_2D_r = Point(self.horiz_2D_s.distance(self.horiz_2D_r), self.r.z, 0)
        self.vert_2D_s_r_segment = Segment(self.vert_2D_s, self.vert_2D_r)
        self.vert_2D_bar_cross_point = Point(
            self.horiz_2D_s.distance(self.horiz_2D_intersect),
            self.bar_cross_point3D.z,
            0,
        )
        self.vert_2D_bar_ray = Ray(
            self.vert_2D_bar_cross_point, self.vert_2D_bar_cross_point + Point(0, -1, 0)
        )
        try:
            self.vert_2D_intersect = self.vert_2D_s_r_segment.intersection(
                self.vert_2D_bar_ray
            )[0]
        except IndexError:
            self.vert_2D_intersect = None

    def get_attr_for_graph(self):
        dist_source2receiver_horizontal = self.horiz_2D_s.distance(self.horiz_2D_r)
        dist_source2bar_horizontal = self.horiz_2D_s.distance(self.horiz_2D_intersect)
        dist_source2receiver_propogation = self.s_r.length
        dist_source2barrier_top = self.s.distance(self.bar_cross_point3D)
        dist_receiver2barrier_top = self.r.distance(self.bar_cross_point3D)
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
        dist_source2barrier_top = self.s.distance(self.bar_cross_point3D)
        dist_receiver2barrier_top = self.r.distance(self.bar_cross_point3D)
        pld_1 = (
            dist_source2barrier_top
            + dist_receiver2barrier_top
            - dist_source2receiver_propogation
        )
        # end legacy section

        pld_2 = (
            self.s.distance(self.bar_cross_point3D)
            + self.r.distance(self.bar_cross_point3D)
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

    def update_barrier_cross_point_3D_attr(self):
        vert_3Dline_at_intersect = Line(
            self.horiz_2D_intersect, self.horiz_2D_intersect + Point(0, 0, 1)
        )
        bar_cross_3Dpoint = vert_3Dline_at_intersect.intersection(self)[0]
        s_r_cross_3Dpoint = vert_3Dline_at_intersect.intersection(self.s_r)[0]

        # testing if line of sight is broken vertically
        if s_r_cross_3Dpoint.z < bar_cross_3Dpoint.z:
            raise Exception("barrier fails EASY vertical test")

        self.bar_cross_point3D = Point(
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

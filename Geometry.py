from sympy import Point, Line as sympy_Line, intersection
import math


class Coordinate:
    """3 dimensional coordinate object."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z

    def get_coords(self) -> tuple[float, float, float]:
        """returns the x, y, and z coordinates of the point."""
        return self.x, self.y, self.z

    def set_coords(self, *args) -> None:
        """take in x, y, z as floats or Coordinate object"""
        if len(args) == 1 and isinstance(args[0], Coordinate):
            coord = args[0]
            self.x, self.y, self.z = coord.x, coord.y, coord.z
        elif (
            len(args) == 3
            and isinstance(args[0], float)
            and isinstance(args[1], float)
            and isinstance(args[2], float)
        ):
            self.x, self.y, self.z = args[0], args[1], args[2]

    def get_distance(self, other_point) -> float:
        return math.sqrt(
            (self.x - other_point.x) ** 2
            + (self.y - other_point.y) ** 2
            + (self.z - other_point.z) ** 2
        )

    def move_to(self, destination: type["Coordinate"]) -> None:
        self.x = destination.x, self.y = destination.y, self.z = destination.z

    def move_by(self, x: float, y: float, z: float) -> None:
        self.x += x
        self.y += y
        self.z += z

    def __add__(self, other_point) -> type["Coordinate"]:
        return Coordinate(
            self.x + other_point.x, self.y + other_point.y, self.z + other_point.z
        )

    def __sub__(self, other_point) -> type["Coordinate"]:
        return Coordinate(
            self.x - other_point.x, self.y - other_point.y, self.z - other_point.z
        )

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Line:
    """A line object that can be used to calculate slope, length, and angle."""

    def __init__(self, start_coords: Coordinate, end_coords: Coordinate) -> None:
        self.start = start_coords
        self.end = end_coords

    def get_start(self) -> Coordinate:
        return self.start.get_coords()

    def get_end(self) -> Coordinate:
        return self.end.get_coords()

    def set_start(self, new_start: Coordinate) -> None:
        self.start = new_start

    def set_end(self, new_end: Coordinate) -> None:
        self.end = new_end

    def get_length(self) -> float:
        return self.start.get_distance(self.end)

    def get_xy_slope(self) -> float:
        try:
            return (self.end.y - self.start.y) / (self.end.x - self.start.x)
        except ZeroDivisionError:
            return float("inf")

    def get_y_intercept(self) -> float:
        """TODO fix when slope is infinite"""
        x, y = self.start.x, self.start.y
        m = self.get_xy_slope()
        b = y - m * x
        return b

    def get_xy_intersection(self, other: type["Line"]) -> tuple[float, float]:
        """returns the intersection coordinates of 2 lines."""
        # m0, b0 = self.get_xy_slope(), self.get_y_intercept()
        # m1, b1 = other_line.get_xy_slope(), other_line.get_y_intercept()
        # if m0 == m1:
        #     return None
        # intersection_x = (b1 - b0) / (m0 - m1)
        # intersection_y = m0 * intersection_x + b0
        l1 = sympy_Line(Point(self.start.x, self.start.y), Point(self.end.x, self.end.y))
        l2 = sympy_Line(Point(other.start.x, other.start.y), Point(other.end.x, other.end.y))
        intersection_point = intersection(l1, l2)
        intersection_x, intersection_y = intersection_point[0].x, intersection_point[0].y
        return (intersection_x, intersection_y)

    def get_center_coords(self):
        return (
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
            (self.start.z + self.end.z) / 2,
        )

    def move_to(self, destination: Coordinate) -> None:
        """Moves the line to the destination coordinates. Move is relative to the start coordinates of the line."""
        """ TODO TEST THIS"""
        movement = destination - self.start
        self.end += movement
        self.start = destination

    def move_by(self, x: float, y: float, z: float) -> None:
        self.start.move_by(x, y, z)
        self.end.move_by(x, y, z)

    def lies_on_point(self, q: Coordinate) -> bool:
        """
        https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'
        """
        if (
            (q.x <= max(self.start.x, self.end.x))
            and (q.x >= min(self.start.x, self.end.x))
            and (q.y <= max(self.start.y, self.end.y))
            and (q.y >= min(self.start.y, self.end.y))
        ):
            return True
        return False

    # def get_center_coords_xy(self):
    #     return ((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    def get_delta_x(self):
        return abs(self.end.x - self.start.x)

    def get_delta_y(self):
        return abs(self.end.y - self.start.y)

    def get_angle_xy(self):
        return math.atan2(self.get_delta_x(), self.get_delta_y())

    def rotate_xy(self, angle: float, pivot: Coordinate):
        """
        rotates the line around the pivot point. if no pivot point is given, the line will rotate around its center.
        rotation angle is in radians.
        """
        # if angle == None:
        #     angle = math.pi / 2
        trans_x0 = self.start.x - pivot.x
        trans_x1 = self.end.x - pivot.x
        trans_y0 = self.start.y - pivot.y
        trans_y1 = self.end.y - pivot.y

        self.start.x = trans_x0 * math.cos(angle) - trans_y0 * math.sin(angle)
        self.end.x = trans_x1 * math.cos(angle) - trans_y1 * math.sin(angle)
        self.start.y = trans_x0 * math.sin(angle) + trans_y0 * math.cos(angle)
        self.end.y = trans_x1 * math.sin(angle) + trans_y1 * math.cos(angle)

        self.start.x += pivot.x
        self.end.x += pivot.x
        self.start.y += pivot.y
        self.end.y += pivot.y

    @staticmethod
    def on_segment(p, q, r):
        """
        https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        Given three colinear points p, q, r, the function checks if
        point q lies on line segment 'pr'
        """
        if (
            (q.x <= max(p.x, r.x))
            and (q.x >= min(p.x, r.x))
            and (q.y <= max(p.y, r.y))
            and (q.y >= min(p.y, r.y))
        ):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        """
        https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        to find the orientation of an ordered triplet (p,q,r)
        function returns the following values:
        0 : Colinear points
        1 : Clockwise points
        2 : Counterclockwise

        See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        for details of below formula.
        """

        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if val > 0:  # Clockwise orientation
            return 1
        elif val < 0:  # Counterclockwise orientation
            return 2
        else:  # Colinear orientation
            return 0

    def intersects(self, other_line: type["Line"]):
        """
        #https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        # The main function that returns true if the line segment 'p1q1' and 'p2q2' intersect.
        """
        p1, q1 = self.start, self.end
        p2, q2 = other_line.start, other_line.end

        # Find the 4 orientations required for
        # the general and special cases
        o1 = Line.orientation(p1, q1, p2)
        o2 = Line.orientation(p1, q1, q2)
        o3 = Line.orientation(p2, q2, p1)
        o4 = Line.orientation(p2, q2, q1)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # Special Cases

        # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
        if (o1 == 0) and Line.on_segment(p1, p2, q1):
            return True

        # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
        if (o2 == 0) and Line.on_segment(p1, q2, q1):
            return True

        # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
        if (o3 == 0) and Line.on_segment(p2, p1, q2):
            return True

        # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
        if (o4 == 0) and Line.on_segment(p2, q1, q2):
            return True

        # If none of the cases
        return False

    # def move_vertical(self, y_amount) -> None:
    #     self.y0 += y_amount
    #     self.y1 += y_amount

    # def move_horizontal(self, x_amount) -> None:
    #     self.x0 += x_amount
    #     self.x1 += x_amount

    # def move_elevation(self, z_amount) -> None:
    #     self.z0 += z_amount
    #     self.z1 += z_amount

    # def angle_between_2_lines(self, other_line: type["Line"]) -> float:
    #     """returns the angle in degrees between to lines"""
    #     m0 = self.get_slope()
    #     m1 = other_line.get_slope()
    #     return math.degrees(math.atan((m1 - m0) / (1 + (m1 * m0))))

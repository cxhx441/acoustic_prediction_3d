import math


class Coordinate:
    """3 dimensional coordinate object."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z

    def get_coords(self) -> tuple[float, float, float]:
        """returns the x, y, and z coordinates of the point."""
        return self.x, self.y, self.z

    def set_coords(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z

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

    def get_start_coords(self) -> Coordinate:
        return self.start.get_coords()

    def get_end_coords(self) -> Coordinate:
        return self.end.get_coords()

    def set_start_point(self, new_start: Coordinate) -> None:
        self.start = new_start

    def set_end_point(self, new_end: Coordinate) -> None:
        self.end = new_end

    def get_length(self) -> float:
        return self.start.get_distance(self.end)

    def get_xy_slope(self) -> float:
        #return (self.y1 - self.y0) / (self.x1 - self.x0)
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def get_y_intercept(self) -> float:
        x, y = self.get_start_coords()
        m = self.get_xy_slope()
        b = y - m * x
        return b

    def get_xy_intersection_of_2_lines(
        self, other_line: type["Line"]
    ) -> tuple[float, float]:
        """returns the intersection coordinates of 2 lines."""
        m0, b0 = self.get_xy_slope(), self.get_y_intercept()
        m1, b1 = other_line.get_xy_slope(), other_line.get_y_intercept()
        intersection_x = (b1 - b0) / (m0 - m1)
        intersection_y = m0 * intersection_x + b0
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

import math


class Point:
    def __init__(self, coords: tuple[float, float, float]) -> None:
        self.x, self.y, self.z = coords

    def get_coords(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def set_coords(self, coords: tuple[float, float, float]):
        self.x, self.y, self.z = coords

    def get_distance(self, other_point) -> float:
        return math.sqrt(
            (self.x - other_point.x) ** 2
            + (self.y - other_point.y) ** 2
            + (self.z - other_point.z) ** 2
        )

class Line:
    """A line object that can be used to calculate slope, length, and angle."""

    def __init__(
        self,
        start_coords: "Point",
        end_coords: "Point"
    ) -> None:
        self.start = start_coords
        self.end = end_coords

    def get_start_coords(self) -> "Point":
        return self.start

    def get_end_coords(self) -> "Point":
        return self.end

    def set_start_coords(self, new_start: "Point") -> None:
        self.start = Point(new_start)

    def set_end_coords(self, new_end: "Point") -> None:
        self.end = Point(new_end)

    def get_length(self):
        return self.start.get_distance(self.end)

    def get_slope(self):
        return (self.y1-self.y0) / (self.x1-self.x0)

    def get_center_coords(self):
        return (self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2, (self.start.z + self.end.z) / 2

    def move(self, destination_coord) -> None:
        """Moves the line to the destination coordinates. Move is relative to the start coordinates of the line."""
        movement_coords = (
            destination_coord[0] - self.start.x,
            destination_coord[1] - self.start.y,
        )
        new_start_coords = (
            self.start.x + movement_coords[0],
            self.start.y + movement_coords[1],
            self.start.z
        )
        new_end_coords = (
            self.end.x + movement_coords[0],
            self.end.y + movement_coords[1],
            self.end.z
        )

        self.set_start_coords(new_start_coords)
        self.set_end_coords(new_end_coords)

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

    # def get_intersection_of_2_lines(
    #     self, other_line: type["Line"]
    # ) -> tuple[float, float]:
    #     """Returns the intersection coordinate of 2 lines. meant for use when drawing reflection rays."""
    #     # if reflector horizontal
    #     if self.get_start_coords()[1] == self.get_end_coords()[1]:
    #         print("horiz")
    #         return (other_line.get_start_coords()[0], self.get_start_coords()[1])
    #     # if reflector vertical
    #     elif self.get_start_coords()[0] == self.get_end_coords()[0]:
    #         print("vert")
    #         return (self.get_start_coords()[0], other_line.get_start_coords()[1])
    #     else:
    #         m0, b0 = self.get_slope(), self.get_y_intercept()
    #         m1, b1 = other_line.get_slope(), other_line.get_y_intercept()
    #         x_int = (b1 - b0) / (m0 - m1)
    #         return (x_int, m0 * x_int + b0)

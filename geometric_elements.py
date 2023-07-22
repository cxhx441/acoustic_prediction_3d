import math

from pyparsing import line


class Line:
    """A line object that can be used to calculate slope, length, and angle."""

    def __init__(
        self,
        start_coords: tuple[float, float, float],
        end_coords: tuple[float, float, float],
    ) -> None:
        self.x0, self.y0, self.z0 = start_coords
        self.x1, self.y1, self.z1 = end_coords

    def get_start_coords(self) -> tuple[float, float, float]:
        return (self.x0, self.y0, self.z0)

    def get_end_coords(self) -> tuple[float, float, float]:
        return (self.x1, self.y1, self.z1)

    def set_start_coords(self, new_start: tuple[float, float, float]) -> None:
        self.x0, self.y0, self.z0 = new_start

    def set_end_coords(self, new_end: tuple[float, float, float]) -> None:
        self.x1, self.y1, self.z1 = new_end

    def get_delta_x(self) -> float:
        return abs(self.x1 - self.x0)

    def get_delta_y(self) -> float:
        return abs(self.y1 - self.y0)

    def get_delta_z(self) -> float:
        return abs(self.z1 - self.z0)

    def get_length(self):
        return math.sqrt(
            self.get_delta_x() ** 2 + self.get_delta_y() ** 2 + self.get_delta_z() ** 2
        )

    def get_center_coords(self):
        return (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2, (self.z0 + self.z1) / 2

    def move(self, destination_coord) -> None:
        """Moves the line to the destination coordinates. Move is relative to the start coordinates of the line."""
        movement_coords = (
            destination_coord[0] - self.get_start_coords()[0],
            destination_coord[1] - self.get_start_coords()[1],
        )
        new_start_coords = (
            self.get_start_coords()[0] + movement_coords[0],
            self.get_start_coords()[1] + movement_coords[1],
        )
        new_end_coords = (
            self.get_end_coords()[0] + movement_coords[0],
            self.get_end_coords()[1] + movement_coords[1],
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

class Barrier(Line):
    barriers = []

    def __init__(self, start_coords, end_coords) -> None:
        super().__init__(start_coords, end_coords)
        Barrier.barriers.append(self)


class Point:
    def __init__(self, coords) -> None:
        self.x, self.y, self.z = coords

    def get_coords(self):
        return self.x, self.y

    def set_coords(self, coords):
        self.x, self.y, self.z = coords


class Receiver(Point):
    receivers = []

    def __init__(self, coords) -> None:
        super().__init__(coords)
        Receiver.receivers.append(self)


class Source(Point):
    sources = []

    def __init__(self, coords) -> None:
        super().__init__(coords)
        Source.sources.append(self)

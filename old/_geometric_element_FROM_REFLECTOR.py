import math

from pyparsing import line


class Line:
    def __init__(self, start_coords, end_coords) -> None:
        self.x0, self.y0 = start_coords
        self.x1, self.y1 = end_coords

    def get_start_coords(self):
        return (self.x0, self.y0)

    def get_end_coords(self):
        return (self.x1, self.y1)

    def set_start_coords(self, new_start):
        self.x0, self.y0 = new_start

    def set_end_coords(self, new_end):
        (self.x1, self.y1) = new_end

    def get_delta_x(self):
        return abs(self.x1 - self.x0)

    def get_delta_y(self):
        return abs(self.y1 - self.y0)

    def get_slope_intercept_form(self):
        x, y = self.get_start_coords()
        m = self.get_slope()
        b = y - m * x
        return (m, b)

    def get_length(self):
        return (self.get_delta_x(), self.get_delta_y())

    def get_center_coords(self):
        return ((self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2)

    def get_angle(self):
        return math.atan2(self.get_delta_x(), self.get_delta_y())

    def get_slope(self):
        return (self.y1 - self.y0) / (self.x1 - self.x0)

    def rotate(self, pivot=None, angle=None):
        """
        rotates the line around the pivot point. if no pivot point is given, the line will rotate around its center.
        rotation angle is in radians.
        """
        if angle == None:
            angle = math.pi / 2
        new_x0, new_y0 = self.get_start_coords()
        new_x1, new_y1 = self.get_end_coords()
        new_x_mid, new_y_mid = self.get_center_coords()
        if pivot == (new_x0, new_y0) or pivot == None:
            trans_x0 = new_x0 - new_x0
            trans_x1 = new_x1 - new_x0
            trans_y0 = new_y0 - new_y0
            trans_y1 = new_y1 - new_y0
        elif pivot == (new_x1, new_y1):
            trans_x0 = new_x0 - new_x1
            trans_x1 = new_x1 - new_x1
            trans_y0 = new_y0 - new_y1
            trans_y1 = new_y1 - new_y1
        elif pivot == (new_x_mid, new_y_mid):
            trans_x0 = new_x0 - new_x_mid
            trans_x1 = new_x1 - new_x_mid
            trans_y0 = new_y0 - new_y_mid
            trans_y1 = new_y1 - new_y_mid

        self.x0 = trans_x0 * math.cos(angle) - trans_y0 * math.sin(angle)
        self.x1 = trans_x1 * math.cos(angle) - trans_y1 * math.sin(angle)
        self.y0 = trans_x0 * math.sin(angle) + trans_y0 * math.cos(angle)
        self.y1 = trans_x1 * math.sin(angle) + trans_y1 * math.cos(angle)

        if pivot == (new_x0, new_y0) or pivot == None:
            self.x0 += new_x0
            self.x1 += new_x0
            self.y0 += new_y0
            self.y1 += new_y0
        elif pivot == (new_x1, new_y1):
            self.x0 += new_x1
            self.x1 += new_x1
            self.y0 += new_y1
            self.y1 += new_y1
        elif pivot == (new_x_mid, new_y_mid):
            self.x0 += new_x_mid
            self.x1 += new_x_mid
            self.y0 += new_y_mid
            self.y1 += new_y_mid

    def move(self, destination_coord):
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

    def move_vertical(self, y_amount):
        self.y0 += y_amount
        self.y1 += y_amount

    def move_horizontal(self, x_amount):
        self.x0 += x_amount
        self.x1 += x_amount

    def angle_between_2_lines(self, other_line: type["Line"]) -> float:
        """returns the angle in degrees between to lines"""
        m0 = self.get_slope()
        m1 = other_line.get_slope()
        return math.degrees(math.atan((m1 - m0) / (1 + (m1 * m0))))

    def get_intersection_of_2_lines(
        self, other_line: type["Line"]
    ) -> tuple[float, float]:
        """returns the intersection coordinates of 2 lines. meant for use when drawing reflection rays."""
        # if reflector horizontal
        if self.get_start_coords()[1] == self.get_end_coords()[1]:
            print("horiz")
            return (other_line.get_start_coords()[0], self.get_start_coords()[1])
        # if reflector vertical
        elif self.get_start_coords()[0] == self.get_end_coords()[0]:
            print("vert")
            return (self.get_start_coords()[0], other_line.get_start_coords()[1])
        else:
            m0, b0 = self.get_slope_intercept_form()
            m1, b1 = other_line.get_slope_intercept_form()
            x_int = (b1 - b0) / (m0 - m1)
            return (x_int, m0 * x_int + b0)


class Ray(Line):
    rays = []

    def __init__(self, start_coords, end_coords):
        super().__init__(start_coords, end_coords)
        Ray.rays.append(self)

    def copy(self):
        return Ray(self.get_start_coords(), self.get_end_coords())

    def get_reflected_ray(self, ray_obj, angle):
        return Ray(self.get_start_coords(), self.get_end_coords())

    def extend(self, room_size):
        x0, y0 = self.get_start_coords()
        x1, y1 = self.get_end_coords()
        # going left
        if x0 > x1:
            x_towidth = 0
            m_towidth, b_towidth = self.get_slope_intercept_form()
            y_towidth = m_towidth * x_towidth + b_towidth
        # going right
        elif x0 < x1:
            x_towidth = room_size[0]
            m_towidth, b_towidth = self.get_slope_intercept_form()
            y_towidth = m_towidth * x_towidth + b_towidth
        # going down
        if y0 < y1:
            y_toheight = room_size[1]
            m_toheight, b_toheight = self.get_slope_intercept_form()
            x_toheight = (y_toheight - b_toheight) / m_toheight
        # going up
        elif y0 > y1:
            y_toheight = 0
            m_toheight, b_toheight = self.get_slope_intercept_form()
            x_toheight = (y_toheight - b_toheight) / m_toheight

        len_toheight = ((y_toheight - y0) ** 2 + (x_toheight - x0) ** 2) ** 0.5
        len_towidth = ((y_towidth - y0) ** 2 + (x_towidth - x0) ** 2) ** 0.5
        if len_toheight < len_towidth:
            self.set_end_coords((x_toheight, y_toheight))
        else:
            self.set_end_coords((x_towidth, y_towidth))


class Reflector(Line):
    reflectors = []

    def __init__(self, start_coords, end_coords):
        super().__init__(start_coords, end_coords)
        Reflector.reflectors.append(self)

    def copy(self):
        return Reflector(self.get_start_coords(), self.get_end_coords())

    def move_up(self, y):
        self.move_vertical(-y)

    def move_down(self, y):
        self.move_vertical(y)

    def move_right(self, x):
        self.move_horizontal(x)

    def move_left(self, x):
        self.move_horizontal(-x)


class Point:
    def __init__(self, coords) -> None:
        self.x_pos, self.y_pos = coords

    def get_coords(self):
        return self.x_pos, self.y_pos

    def move_up(self, y):
        self.y_pos -= y

    def move_down(self, y):
        self.y_pos += y

    def move_right(self, x):
        self.x_pos += x

    def move_left(self, x):
        self.x_pos -= x


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

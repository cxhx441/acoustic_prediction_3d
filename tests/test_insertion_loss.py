import unittest
from InsertionLoss import (
    InsertionLoss,
    HORIZONTAL_ERR,
    VERTICAL_ERR,
    POINT_3D_ERR,
    GRAZING_ERR,
)
from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from OctaveBands import OctaveBands
from sympy.geometry import Point, Segment

"""
# TODO
test perpendicular s_r to bar gives same answer when sliding intersection point
test rotations give same answer
"""


def get_random_source():
    ob = OctaveBands.get_rand_ob()
    return Source(Point(0, 0, 0), 100, 3, ob)


class TestInsertionLoss(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True)

    def test_2(self):
        """Test s_r grazes barrier start"""
        s = get_random_source()
        s.geo = Point(0, 0, 0)
        r = Receiver(Point(10, 10, 0))
        b = Barrier(Segment((5, 5, 0), (5, 0, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

    def test_3(self):
        """Test s_r grazes barrier end"""
        s = get_random_source()
        s.geo = Point(0, 0, 0)
        r = Receiver(Point(10, 10, 0))
        b = Barrier(Segment((5, 0, 0), (5, 5, 0)))

        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

    def test_4(self):
        """Test barrier grazes s"""
        s = get_random_source()
        s.geo = Point(5, 5, 0)
        r = Receiver(Point(5, 0, 0))
        b = Barrier(Segment((0, 0, 0), (10, 10, 0)))

        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

    def test_5(self):
        """Test barrier grazes r"""
        s = get_random_source()
        s.geo = Point(5, 0, 0)
        r = Receiver(Point(5, 5, 0))
        b = Barrier(Segment((0, 0, 0), (10, 10, 0)))

        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

    def test_6(self):
        """Test miss in just horizontal section"""
        s = get_random_source()
        s.geo = Point(5, 0, 5)
        r = Receiver(Point(20, 10, 5))
        b = Barrier(Segment((0, 5, 6), (10, 5, 6)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)

    def test_8(self):
        """Test miss in just vertical section"""
        s = get_random_source()
        s.geo = Point(5, 0, 5)
        r = Receiver(Point(5, 10, 15))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, POINT_3D_ERR)

    def test_9(self):
        """Test miss in vertical & horizontal section"""
        s = get_random_source()
        s.geo = Point(5, 0, 5)
        r = Receiver(Point(20, 10, 15))
        b = Barrier(Segment((0, 5, 6), (10, 5, 6)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)

    def test_12(self):
        """Test pld == 0"""
        s = get_random_source()
        s.geo = Point(5, 0, 0)
        r = Receiver(Point(5, 10, 10))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 0)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, None)

    def test_13(self):
        """Test no octave band levels gives no fresnel IL"""
        s = Source(Point(5, 0, 0), 100, 3)
        s.octave_band_levels = None
        r = Receiver(Point(5, 8, 0))
        b = Barrier(Segment((0, 4, 3), (8, 4, 3)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 2)
        self.assertEqual(il.il_ari, 10)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, None)

    def test_15(self):
        """Test parallel s_r and bar give no IL"""
        s = get_random_source()
        s.geo = Point(5, 0, 0)
        r = Receiver(Point(5, 10, 10))
        b = Barrier(Segment((6, 10, 10), (6, 0, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 0)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)


if __name__ == "__main__":
    unittest.main()

import unittest
from Source import Source
from Receiver import Receiver
from OctaveBands import OctaveBands
from sympy.geometry import Point, Segment


def get_random_source():
    ob = OctaveBands.get_rand_ob()
    return Source(Point(0, 0, 0), 100, 3, ob)


class TestSource(unittest.TestCase):
    def test_create_source(self):
        """Test you can create a source"""
        ob = OctaveBands.get_rand_ob()
        s = Source(Point(0, 0, 0), 100, 3)
        s = Source(Point(0, 0, 0), 100, 3, ob)

    def test_2(self):
        """test you can make a segment out of a source and receiver"""
        s = get_random_source()
        r = Receiver(Point(10, 10, 0))
        seg = Segment(s.geo, r.geo)
        self.assertIsInstance(seg, Segment)


if __name__ == "__main__":
    unittest.main()

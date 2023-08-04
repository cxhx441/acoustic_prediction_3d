import unittest
from InsertionLoss import InsertionLoss
from Source import Source
from Receiver import Receiver
from Barrier import Barrier
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

    def test_2(self):
        """test you can make a segment out of a source and receiver"""
        s = get_random_source()
        r = Receiver(Point(10, 10, 0))
        seg = Segment(s.geo, r.geo)
        self.assertIsInstance(seg, Segment)

class TestReceiver(unittest.TestCase):
    def test_create_receiver(self):
        """Test you can create a receiver"""
        r = Receiver(Point(0, 0, 0))
        self.assertIsInstance(r, Receiver)


class TestBarrier(unittest.TestCase):
    def test_create_barrier(self):
        """Test you can create a barrier"""
        b = Barrier(Segment((0, 0, 0), (1, 1, 1)))
        self.assertIsInstance(b, Barrier)


class TestInsertionLoss(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True)

    def test_2(self):
        """Test s_r grazes barrier start"""
        s = get_random_source()
        s.geo = Point(0, 0, 0)
        r = Receiver(Point(10, 10, 0))
        b = Barrier(Segment((5, 5, 0), (5, 0, 0)))

        self.assertEqual(InsertionLoss(s, r, b).il_ari, 0)
        self.assertEqual(InsertionLoss(s, r, b).il_fresnel, 0)

    def test_3(self):
        """Test barrier end grazes s_r"""
        self.assertTrue(False)

    def test_4(self):
        """Test s grazes barrier"""
        self.assertTrue(False)

    def test_5(self):
        """Test r grazes barrier"""
        self.assertTrue(False)

    def test_6(self):
        """Test miss in just horizontal section"""
        self.assertTrue(False)

    def test_8(self):
        """Test miss in just vertical section"""
        self.assertTrue(False)

    def test_9(self):
        """Test miss in vertical & horizontal section"""
        self.assertTrue(False)

    def test_11(self):
        """Test miss in bar_cross_point 3D == None ... TODO think we'll never reach this"""
        self.assertTrue(False)

    def test_12(self):
        """Test pld == 0"""
        self.assertTrue(False)

    def test_13(self):
        """Test no octave band levels gives no fresnel IL"""
        self.assertTrue(False)

    def test_14(self):
        """Test no octave band levels still gives ari IL"""
        self.assertTrue(False)

    def test_15(self):
        """Test parallel s_r and bar give no IL"""
        self.assertTrue(False)

    """
    # TODO
    test perpendicular s_r to bar gives same answer when sliding intersection point
    test rotations give same answer
    """


if __name__ == "__main__":
    unittest.main()

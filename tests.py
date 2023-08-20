import random
import unittest
from InsertionLoss import (
    InsertionLoss,
    HORIZONTAL_ERR,
    VERTICAL_ERR,
    POINT_3D_ERR,
    GRAZING_ERR,
    dbsum,
)
from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from OctaveBands import OctaveBands
from sympy.geometry import Point, Segment
from acoustics.decibel import dbsum as dbsum_acoustics


def get_random_source():
    ob = OctaveBands.get_rand_ob()
    return Source(Point(0, 0, 0), 100, 3, ob)


class TestDecibelAdder(unittest.TestCase):
    def test_1(self):
        dBs = [10, 100]
        self.assertEqual(dbsum(dBs), dbsum_acoustics(dBs))

    def test_2(self):
        dBs = [10, 20, 30]
        self.assertEqual(dbsum(dBs), 30.453229787866576)

    def test_3(self):
        dBs = [10, -10]
        self.assertEqual(dbsum(dBs), 10.043213737826427)

    def test_4(self):
        dBs = [10] * 4
        self.assertEqual(dbsum(dBs), 16.02059991327962)

    def test_5_random(self):
        def random_dB_list():
            length = random.randint(1, 100)
            ret_list = [None] * length
            for i in range(length):
                ret_list[i] = random.uniform(-200.0, 200.0)
            return ret_list

        for _ in range(100):
            with self.subTest():
                dBs = random_dB_list()
                self.assertAlmostEqual(dbsum(dBs), dbsum_acoustics(dBs), places=5)


class TestOctaveBands(unittest.TestCase):
    def test_create_ob(self):
        """Test you can create an octave band"""
        ob = OctaveBands([100] * 8)
        self.assertIsInstance(ob, OctaveBands)

    def test_create_static_ob(self):
        """Test you can create an octave band"""
        ob = OctaveBands.get_static_ob(100)
        self.assertIsInstance(ob, OctaveBands)

    def test_create_rand_ob(self):
        """Test you can create an octave band"""
        ob = OctaveBands.get_rand_ob()
        self.assertIsInstance(ob, OctaveBands)

    def test_dBA(self):
        """Test dBA is coming out right from octave bands"""
        ob = OctaveBands.get_static_ob(100)
        self.assertAlmostEqual(ob.get_dBA(), 107, delta=0.5)
        ob = OctaveBands((71, 41, 26, 93, 75, 44, 61, 58))
        self.assertAlmostEqual(ob.get_dBA(), 90, delta=0.5)


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

    def test_16(self):
        """Mukilteo sheet For Pres-grnd"""
        ob = OctaveBands((69, 67, 68, 70, 65, 62, 57, 54))
        s = Source(Point(0, 0, 9), 71, 30, ob)
        r = Receiver(Point(0, 68, 20))
        b = Barrier(Segment((-10, 13, 19), (10, 13, 19)))
        il = InsertionLoss(s, r, b)
        self.assertAlmostEqual(il.pld, 2.5263, places=4)
        self.assertEqual(il.il_ari, 11)
        self.assertAlmostEqual(il.il_fresnel, 17.26378, places=5)

    def test_17(self):
        """Mukilteo sheet For Pres-6ft"""
        ob = OctaveBands((69, 67, 68, 70, 65, 62, 57, 54))
        s = Source(Point(0, 0, 22), 71, 30, ob)
        r = Receiver(Point(0, 184.61, 22))
        b = Barrier(Segment((-10, 6, 25.25), (10, 6, 25.25)))
        il = InsertionLoss(s, r, b)
        self.assertAlmostEqual(il.pld, 0.8532, places=4)
        self.assertEqual(il.il_ari, 6)
        self.assertAlmostEqual(il.il_fresnel, 13.17744, places=5)

    """
    # TODO
    test perpendicular s_r to bar gives same answer when sliding intersection point
    test rotations give same answer
    """


if __name__ == "__main__":
    unittest.main()
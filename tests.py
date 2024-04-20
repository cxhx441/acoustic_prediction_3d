import random
import unittest
from InsertionLoss import (
    InsertionLoss,
    HORIZONTAL_ERR,
    # VERTICAL_ERR,
    POINT_3D_ERR,
    GRAZING_ERR,
    dbsum,
)
from SoundField import SoundField
from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from OctaveBands import OctaveBands
from sympy.geometry import Point, Segment
# from acoustics.decibel import dbsum as dbsum_acoustics
import math
from itertools import permutations


def get_random_source():
    ob = OctaveBands.get_rand_ob()
    return Source(Point(0, 0, 0), 100, 3, ob)


class TestDecibelAdder(unittest.TestCase):
    def test_1(self):
        dBs = [10, 100]
        self.assertAlmostEqual(dbsum(dBs), 100.00000000434295, places=5)

    def test_2(self):
        dBs = [10, 20, 30]
        self.assertAlmostEqual(dbsum(dBs), 30.453229787866576, places=5)

    def test_3(self):
        dBs = [10, -10]
        self.assertAlmostEqual(dbsum(dBs), 10.043213737826427, places=5)

    def test_4(self):
        dBs = [10] * 4
        self.assertAlmostEqual(dbsum(dBs), 16.02059991327962, places=5)

    # def test_5_random(self):
    #     def random_dB_list():
    #         length = random.randint(1, 100)
    #         ret_list = [None] * length
    #         for i in range(length):
    #             ret_list[i] = random.uniform(-200.0, 200.0)
    #         return ret_list

    #     for _ in range(100):
    #         with self.subTest():
    #             dBs = random_dB_list()
    #             self.assertAlmostEqual(dbsum(dBs), dbsum_acoustics(dBs), places=5)


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
        self.assertIsInstance(s, Source)

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
        s.ob_lvls = None
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


class TestApp(unittest.TestCase):
    def test_create_sfield(self):
        sfield = SoundField()
        self.assertIsInstance(sfield, SoundField)

    def test_running_sfield(self):
        """Test simple sfield setup"""
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(10, 0, 0))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))

        sfield.add(s)
        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.sound_path_matrix), len(sfield.sources))

        sfield.add(r)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

        sfield.add(b)
        self.assertEqual(len(sfield.barriers), 1)

        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 1)

    def test_add_remove_srb_to_sfield(self):
        """ test you can add/remove source/receiver/barriers without error. """
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(10, 0, 0))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))

        sfield.remove({s, r, b})

        sfield.add({s, r, b})
        sfield.add({s, r, b})

        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 1)
        self.assertEqual(len(sfield.sound_path_matrix), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

        sfield.remove(s)
        self.assertEqual(len(sfield.sources), 0)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 1)
        self.assertEqual(len(sfield.sound_path_matrix), 0)

        sfield.add(s)
        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 1)
        self.assertEqual(len(sfield.sound_path_matrix), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

        sfield.remove(r)
        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 0)
        self.assertEqual(len(sfield.barriers), 1)
        self.assertEqual(len(sfield.sound_path_matrix), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 0)

        sfield.add(r)
        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 1)
        self.assertEqual(len(sfield.sound_path_matrix), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

        sfield.remove(b)
        self.assertEqual(len(sfield.sources), 1)
        self.assertEqual(len(sfield.receivers), 1)
        self.assertEqual(len(sfield.barriers), 0)
        self.assertEqual(len(sfield.sound_path_matrix), 1)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

        sfield.remove({s, r, b})
        self.assertEqual(len(sfield.sources), 0)
        self.assertEqual(len(sfield.receivers), 0)
        self.assertEqual(len(sfield.barriers), 0)
        self.assertEqual(len(sfield.sound_path_matrix), 0)

    def test_permutations_of_add_remove_srb_to_sfield(self):
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(10, 0, 0))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))

        perms = permutations([s, r, b])
        # remove in perm order
        for p in perms:
            sfield.add({s, r, b})
            self.assertEqual(len(sfield.sources), 1)
            self.assertEqual(len(sfield.receivers), 1)
            self.assertEqual(len(sfield.barriers), 1)
            self.assertEqual(len(sfield.sound_path_matrix), 1)
            self.assertEqual(len(sfield.sound_path_matrix[0]), 1)

            sfield.remove(p[0])
            sfield.remove(p[1])
            sfield.remove(p[2])

            self.assertEqual(len(sfield.sources), 0)
            self.assertEqual(len(sfield.receivers), 0)
            self.assertEqual(len(sfield.barriers), 0)
            self.assertEqual(len(sfield.sound_path_matrix), 0)

        # add in perm order
        for p in perms:
            sfield.remove({s, r, b})
            self.assertEqual(len(sfield.sources), 0)
            self.assertEqual(len(sfield.receivers), 0)
            self.assertEqual(len(sfield.barriers), 0)
            self.assertEqual(len(sfield.sound_path_matrix), 0)

            sfield.add(p[0])
            sfield.add(p[1])
            sfield.add(p[2])

            self.assertEqual(len(sfield.sources), 1)
            self.assertEqual(len(sfield.receivers), 1)
            self.assertEqual(len(sfield.barriers), 1)
            self.assertEqual(len(sfield.sound_path_matrix), 1)
            self.assertEqual(len(sfield.sound_path_matrix[0]), 1)
    def test_barrier_deletion_removes_from_sound_path(self):
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(10, 0, 0))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))

        sfield.add({s, r, b})
        self.assertEqual(len(sfield.sound_path_matrix[0][0].allowed_barriers), 0)

        sfield.set_allowed_barriers(s, r, {b})
        self.assertEqual(len(sfield.sound_path_matrix[0][0].allowed_barriers), 1)
        self.assertTrue(b in sfield.sound_path_matrix[0][0].allowed_barriers)
        sfield.remove(b)
        self.assertEqual(len(sfield.sound_path_matrix[0][0].allowed_barriers), 0)

    def test_mult_sr_adds_removes(self):
        sfield = SoundField()
        s0 = Source(Point(0, 0, 0), 100, 10)
        s1 = Source(Point(0, 0, 0), 100, 10)
        s2 = Source(Point(0, 0, 0), 100, 10)
        r0 = Receiver(Point(10, 0, 0))
        r1 = Receiver(Point(10, 0, 0))
        r2 = Receiver(Point(10, 0, 0))
        r3 = Receiver(Point(10, 0, 0))
        b0 = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        b1 = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        b2 = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        s_set = {s0, s1, s2}
        r_set = {r0, r1, r2, r3}
        b_set = {b0, b1, b2}
        all_set = s_set | r_set | b_set

        def _add_in_order():
            sfield.add(s0)
            sfield.add(s1)
            sfield.add(s2)
            sfield.add(b0)
            sfield.add(b1)
            sfield.add(b2)
            sfield.add(r0)
            sfield.add(r1)
            sfield.add(r2)
            sfield.add(r3)

        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sfield.add(all_set)
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)

        sp = sfield.sound_path_matrix[0][1]
        sfield.remove(r0)
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 3)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp)

        sfield.add(r0)
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)


        sfield.remove(all_set)
        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sp0 = sfield.sound_path_matrix[0][0]
        sp2 = sfield.sound_path_matrix[0][2]
        sfield.remove(r1)
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 3)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp0)
        self.assertEqual(sfield.sound_path_matrix[0][1], sp2)

        sfield.remove(all_set)
        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sp0 = sfield.sound_path_matrix[0][0]
        sp1 = sfield.sound_path_matrix[0][1]
        sfield.remove(r2)
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 3)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp0)
        self.assertEqual(sfield.sound_path_matrix[0][1], sp1)

        sfield.remove(all_set)
        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sp0 = sfield.sound_path_matrix[0][0]
        sp1 = sfield.sound_path_matrix[2][0]
        sfield.remove(s1)
        self.assertEqual(len(sfield.sound_path_matrix), 2)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp0)
        self.assertEqual(sfield.sound_path_matrix[1][0], sp1)

        sfield.remove(all_set)
        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sp0 = sfield.sound_path_matrix[0][0]
        sp1 = sfield.sound_path_matrix[1][0]
        sfield.remove(s2)
        self.assertEqual(len(sfield.sound_path_matrix), 2)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp0)
        self.assertEqual(sfield.sound_path_matrix[1][0], sp1)

        sfield.remove(all_set)
        _add_in_order()
        self.assertEqual(len(sfield.sound_path_matrix), 3)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        sp0 = sfield.sound_path_matrix[1][0]
        sp1 = sfield.sound_path_matrix[2][0]
        sfield.remove(s0)
        self.assertEqual(len(sfield.sound_path_matrix), 2)
        self.assertEqual(len(sfield.sound_path_matrix[0]), 4)
        self.assertEqual(sfield.sound_path_matrix[0][0], sp0)
        self.assertEqual(sfield.sound_path_matrix[1][0], sp1)



    def test_simple_dbA_prediction_no_barrier_1(self):
        """Test that the predicted dBA is same as reference distance if same distance away from source"""
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(10, 0, 0))
        sfield.add({s, r})

        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)

    def test_simple_dbA_prediction_no_barrier_2(self):
        """Test that predicted dBA is -6 when twice the reference distance."""
        sfield = SoundField()
        s = Source(Point(0, 0, 0), 100, 10)
        r = Receiver(Point(20, 0, 0))
        sfield.add({s, r})

        sfield.update_dBA_predictions()
        self.assertAlmostEqual(r.dBA_predicted, 94, 1)

    def test_simple_dbA_prediction_no_barrier_3(self):
        """Test that predicted dBA is +3 when there are two sources equidistant away from source. """
        sfield = SoundField()
        s0 = Source(Point(-10, 0, 0), 100, 10)
        s1 = Source(Point(+10, 0, 0), 100, 10)
        r = Receiver(Point(0, 0, 0))
        sfield.add({s0, s1, r})

        sfield.update_dBA_predictions()
        self.assertAlmostEqual(r.dBA_predicted, 103, 1)

    def test_simple_dbA_prediction_no_barrier_4(self):
        """Test that predicted dBA is +10 when there are 10 sources equidistant away from source. """
        sfield = SoundField()
        for i in range(10):
            sfield._add_source(Source(Point(10, 0, 0), 100, 10))
        r = Receiver(Point(0, 0, 0))
        sfield.add(r)

        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 110)

    def test_simple_dbA_prediction_no_barrier_5(self):
        """ test 2 receivers. """
        sfield = SoundField()
        for i in range(10):
            sfield._add_source(Source(Point(10, 0, 0), 100, 10))
        r0 = Receiver(Point(0, 0, 0))
        r1 = Receiver(Point(-10, 0, 0))
        sfield.add({r0, r1})

        sfield.update_dBA_predictions(r0)
        sfield.update_dBA_predictions(r1)
        self.assertEqual(r0.dBA_predicted, 110)
        self.assertAlmostEqual(r1.dBA_predicted, 104, 1)

        sfield.update_dBA_predictions({r1})
        self.assertAlmostEqual(r1.dBA_predicted, 104, 1)

    def test_2_with_sfield(self):
        """Test s_r grazes barrier start and gives proper dBA prediction."""
        s = Source(Point(0, 0, 0), 100, math.sqrt(10**2 + 10**2))
        r = Receiver(Point(10, 10, 0))
        b = Barrier(Segment((5, 5, 0), (5, 0, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)
        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.remove({s, r, b})
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_3_with_sfield(self):
        """Test s_r grazes barrier end and gives proper dBA prediction."""
        s = Source(Point(0, 0, 0), 100, math.sqrt(10**2 + 10**2))
        r = Receiver(Point(10, 10, 0))
        b = Barrier(Segment((5, 0, 0), (5, 5, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_4_with_sfield(self):
        """Test barrier grazes s"""
        s = Source(Point(5, 5, 0), 100, 5)
        r = Receiver(Point(5, 0, 0))
        b = Barrier(Segment((0, 0, 0), (10, 10, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_5_with_sfield(self):
        """Test barrier grazes r"""
        s = Source(Point(5, 0, 0), 100, 5)
        r = Receiver(Point(5, 5, 0))
        b = Barrier(Segment((0, 0, 0), (10, 10, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, GRAZING_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_6_with_sfield(self):
        """Test miss in just horizontal section"""
        s = Source(Point(5, 0, 5), 100, math.sqrt(15**2 + 10**2))
        r = Receiver(Point(20, 10, 5))
        b = Barrier(Segment((0, 5, 6), (10, 5, 6)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)


    def test_8_with_sfield(self):
        """Test miss in just vertical section"""
        s = Source(Point(5, 0, 5), 100, math.sqrt(10**2 + 10**2))
        r = Receiver(Point(5, 10, 15))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, POINT_3D_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)


    def test_9_with_sfield(self):
        """Test miss in vertical & horizontal section"""
        s = Source(Point(5, 0, 5), 100, math.sqrt(15**2 + 10**2 + 10**2))
        r = Receiver(Point(20, 10, 15))
        b = Barrier(Segment((0, 5, 6), (10, 5, 6)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_12_with_sfield(self):
        """Test pld == 0"""
        s = Source(Point(5, 0, 0), 100, math.sqrt(0**2 + 10**2 + 10**2))
        r = Receiver(Point(5, 10, 10))
        b = Barrier(Segment((0, 5, 5), (10, 5, 5)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 0)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, None)
        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_13_with_sfield(self):
        """Test no octave band levels gives no fresnel IL"""
        s = Source(Point(5, 0, 0), 100, math.sqrt(0**2 + 8**2 + 0**2))
        s.ob_lvls = None
        r = Receiver(Point(5, 8, 0))
        b = Barrier(Segment((0, 4, 3), (8, 4, 3)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 2)
        self.assertEqual(il.il_ari, 10)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, None)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 90)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 87)


    def test_15_sfield(self):
        """Test parallel s_r and bar give no IL"""
        s = Source(Point(5, 0, 0), 100, math.sqrt(0**2 + 10**2 + 10**2))
        r = Receiver(Point(5, 10, 10))
        b = Barrier(Segment((6, 10, 10), (6, 0, 0)))
        il = InsertionLoss(s, r, b)
        self.assertEqual(il.pld, 0)
        self.assertEqual(il.il_ari, 0)
        self.assertEqual(il.il_fresnel, 0)
        self.assertEqual(il.error, HORIZONTAL_ERR)

        sfield = SoundField()
        sfield.add({s, r, b})
        sfield.set_allowed_barriers(s, r, {b})
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 100)
        sfield.set_directivity_loss(s, r, 3)
        sfield.update_dBA_predictions()
        self.assertEqual(r.dBA_predicted, 97)

    def test_16_sfield(self):
        """Candela RTU-01 to R1 """
        ob = OctaveBands((88, 89, 85, 85, 83, 78, 74, 68))
        rtu01 = Source(Point(411.14, 250.11, 501.5), 87, 0, ob, q_tested=1, q_installed=2)
        r1 = Receiver(Point(488.64, 40.76, 465))
        w_bar15 = Barrier(Segment((443.43, 53.67, 498.5), (439.2, 262.36, 498.5)))
        il = InsertionLoss(rtu01, r1, w_bar15)
        self.assertAlmostEqual(il.pld,1.125, places=3)
        self.assertAlmostEqual(il.il_ari,7.375, places=0)
        self.assertAlmostEqual(il.il_fresnel, 14.077, places=3)

        sfield = SoundField()
        sfield.add({rtu01, r1, w_bar15})
        sfield.set_allowed_barriers(rtu01, r1, {w_bar15})

        # ari
        sfield.update_dBA_predictions()
        self.assertAlmostEqual(r1.dBA_predicted,35.53, places=2)

        # fresnel
        sfield.set_barrier_method(rtu01, r1, "FRESNEL")
        sfield.update_dBA_predictions()
        self.assertAlmostEqual(r1.dBA_predicted,28.457, places=2)


if __name__ == "__main__":
    unittest.main()

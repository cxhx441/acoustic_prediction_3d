import unittest
from InsertionLoss import InsertionLoss
from Source import Source
from Receiver import Receiver
from Barrier import Barrier
from OctaveBands import OctaveBands


class TestInsertionLoss(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True)

    def test_2(self):
        """Test barrier start grazes s_r"""
        self.assertTrue(False)

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

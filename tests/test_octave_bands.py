import unittest
from OctaveBands import OctaveBands


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

if __name__ == "__main__":
    unittest.main()

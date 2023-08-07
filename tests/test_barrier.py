import unittest
from Barrier import Barrier
from sympy.geometry import Point, Segment


class TestBarrier(unittest.TestCase):
    def test_create_barrier(self):
        """Test you can create a barrier"""
        b = Barrier(Segment((0, 0, 0), (1, 1, 1)))
        self.assertIsInstance(b, Barrier)


if __name__ == "__main__":
    unittest.main()

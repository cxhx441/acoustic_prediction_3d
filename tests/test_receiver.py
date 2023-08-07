import unittest
from Receiver import Receiver
from sympy.geometry import Point


class TestReceiver(unittest.TestCase):
    def test_create_receiver(self):
        """Test you can create a receiver"""
        r = Receiver(Point(0, 0, 0))
        self.assertIsInstance(r, Receiver)


if __name__ == "__main__":
    unittest.main()

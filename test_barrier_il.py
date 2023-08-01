import unittest
import Barrier
import Old_Barrier
from Source import Source, OctaveBands
from Receiver import Receiver
from random import randint, uniform
from Geometry import Coordinate, Line
from tabulate import tabulate
import math


class TestBarrier(unittest.TestCase):
    def test_random_il(self):
        def rand_coord(low, high):
            return Coordinate(
                randint(low, high) / 10,
                randint(low, high) / 10,
                randint(low, high) / 10,
            )

        for i in range(10000):
            ob = OctaveBands.get_rand_ob(0, 100)
            dba = ob.get_dBA()

            # path hits barrier
            # not vertical or horizontal
            # barrier line is vertical
            # barrier line is horizontal
            # s_2_r line is horizontal
            # s_2_r line is vertical
            # path misses barrier
            # horizontally
            # not vertical or horizontal
            # barrier line is vertical
            # barrier line is horizontal
            # s_2_r line is horizontal
            # s_2_r line is vertical
            # vertically
            # not vertical or horizontal
            # barrier line is vertical
            # barrier line is horizontal
            # s_2_r line is horizontal
            # s_2_r line is vertical

            # dba = ob.get_dBA()
            # b_start = Coordinate(5, -1, 5)
            # # b_start = Coordinate(0, 0, 0) # causes error
            # b_end = Coordinate(5, 1, 5)
            # s_coord = Coordinate(1, 0, 1)
            # r_coord = Coordinate(10, 0, 1)

            low, high = -100, 100
            b_start = rand_coord(low, high)
            # b_start = Coordinate(0, 0, 0) # causes error
            b_end = rand_coord(low, high)
            s_coord = rand_coord(low, high)
            r_coord = rand_coord(low, high)

            # # same slope
            # b_start = Coordinate(-4, 4, -2)
            # b_end = Coordinate(-3, 3, -9)
            # s_coord = Coordinate(8, -8, 10)
            # r_coord = Coordinate(-5, 5, 0)

            # # infinite slope
            # b_start = Coordinate(-4, 4, -2)
            # b_end = Coordinate(-3, 3, -9)
            # s_coord = Coordinate(6, 9, 3)
            # r_coord = Coordinate(6, 2, 4)

            # # good case
            # b_start = Coordinate(0, 10, 100)
            # b_end = Coordinate(0, -10, 100)
            # s_coord = Coordinate(-10, 0, 9)
            # r_coord = Coordinate(10, 0, 9)

            s = Source(coords=s_coord, dBA=dba, ref_dist=3.28, octave_band_levels=ob)
            r = Receiver(coords=r_coord)
            b_old = Old_Barrier.Barrier(start=b_start, end=b_end)
            b = Barrier.Barrier(start=b_start, end=b_end)


            print(f"TEST NUMBER {i}")
            b_old_ari = b_old.get_insertion_loss_ARI(s, r)
            b_ari = b.get_insertion_loss(s, r, method="ARI")
            b_old_fres = b_old.get_insertion_loss_OB_fresnel(s, r)
            b_fres = b.get_insertion_loss(s, r, method="Fresnel")
            print(b_old_ari)
            print(b_ari)
            print(b_old_fres)
            print(b_fres)
            print()
            print()
            coords_msg = f"\nb_old.set_start(Coordinate{b_old.start})\nb_old.set_end(Coordinate{b_old.end})\nb.set_start(Coordinate{b.start})\nb.set_end(Coordinate{b.end})\ns.set_coords(Coordinate{s_coord})\nr.set_coords(Coordinate{r_coord})"

            with self.subTest():
                self.assertAlmostEqual(b_old_ari, b_ari, msg=coords_msg)
                self.assertAlmostEqual(b_old_fres, b_fres, msg=coords_msg)
                # TODO need to handle where path length difference = 0

    def test_rotation(self):
        for i in range(1000):
            ob = OctaveBands.get_rand_ob(0, 100)
            dba = ob.get_dBA()

            def rand_coord(low, high):
                return Coordinate(
                    randint(low, high) / 10,
                    randint(low, high) / 10,
                    randint(low, high) / 10,
                )

            low, high = -100, 100
            b_start = rand_coord(low, high)
            b_end = rand_coord(low, high)
            s_coord = rand_coord(low, high)
            r_coord = rand_coord(low, high)

            # # same slope
            # b_start = Coordinate(-4, 4, -2)
            # b_end = Coordinate(-3, 3, -9)
            # s_coord = Coordinate(8, -8, 10)
            # r_coord = Coordinate(-5, 5, 0)

            # # infinite slope
            # b_start = Coordinate(-4, 4, -2)
            # b_end = Coordinate(-3, 3, -9)
            # s_coord = Coordinate(6, 9, 3)
            # r_coord = Coordinate(6, 2, 4)

            # # good case
            # b_start = Coordinate(0.001, 10, 100)
            # b_end = Coordinate(0, -10, 100)
            # s_coord = Coordinate(-10, 0.001, 9)
            # r_coord = Coordinate(10, 0, 9)

            s = Source(coords=s_coord, dBA=dba, ref_dist=3.28, octave_band_levels=ob)
            r = Receiver(coords=r_coord)
            b = Barrier.Barrier(start=b_start, end=b_end)

            b_ari = b.get_insertion_loss(s, r, "ARI")
            b_fres = b.get_insertion_loss(s, r, "Fresnel")

            print("\nTEST NUMBER", i)
            print(f"{b.start}, {b.end} : {s_coord}, {r_coord}")
            # then rotate
            sr_line = Line(s_coord, r_coord)
            xy_intersection = b.get_xy_intersection(sr_line)
            intersection = Coordinate(xy_intersection[0], xy_intersection[1], 0)
            rand_angle = uniform(0, 2 * math.pi)
            b.rotate_xy(rand_angle, intersection)
            sr_line.rotate_xy(rand_angle, intersection)
            s.set_coords = sr_line.start
            r.set_coords = sr_line.end

            print(f"{b.start}, {b.end} : {s_coord}, {r_coord}")
            b_rotated_ari = b.get_insertion_loss(s, r, "ARI")
            b_rotated_fres = b.get_insertion_loss(s, r, "Fresnel")

            if (
                b_ari == 0
                and b_fres == 0
                and b_rotated_ari == 0
                and b_rotated_fres == 0
            ):
                print("all 0s")
                continue

            print(f"{b.start} -> {b.end}")
            print(f"{b_rotated_ari} == \n{b_ari}")
            print(f"{b.start} -> {b.end}")
            print(f"{b_rotated_fres} == \n{b_fres}")
            with self.subTest():
                self.assertEqual(b_rotated_ari, b_ari, msg=f"{b_rotated_ari} != {b_ari}")
                self.assertEqual(
                    b_rotated_fres, b_fres, msg=f"{b_rotated_fres} != {b_fres}"
                )

    def test_rotation_manual(self):
        ob = OctaveBands.get_rand_ob(0, 100)
        dba = ob.get_dBA()

        b = Barrier.Barrier(Coordinate(0.1, -9.3, 7.2), Coordinate(-8.5, 8.7, -2.6))
        s = Source(Coordinate(1.8, -2.0, 5.1), dba, 3.28, octave_band_levels=ob)
        r = Receiver(Coordinate(-8.0, -6.3, -4.9))

        b2 = Barrier.Barrier(
            Coordinate(3.508532156104924, -4.184524701059347, 7.2),
            Coordinate(-16.415033023245357, -3.1787660102288386, -2.6),
        )
        s2 = Source(
            Coordinate(-2.101971902330027, 0.7856105295239173, 5.1),
            dba,
            3.28,
            octave_band_levels=ob,
        )
        r2 = Receiver(Coordinate(-2.985686139648712, -9.87970939754626, -4.9))

        b2_ari = b2.get_insertion_loss(s2, r2, "ARI")
        b2_fres = b2.get_insertion_loss(s2, r2, "Fresnel")

        b_ari = b.get_insertion_loss(s, r, "ARI")
        b_fres = b.get_insertion_loss(s, r, "Fresnel")

        self.assertEqual(b_ari, b2_ari)
        self.assertEqual(b_fres, b2_fres)

    def test_manual(self):
        ob = OctaveBands.get_static_ob(100)
        dba = ob.get_dBA()

        b = Barrier.Barrier(Coordinate(0.1, -9.3, 7.2), Coordinate(-8.5, 8.7, -2.6))
        b_old = Old_Barrier.Barrier(
            Coordinate(0.1, -9.3, 7.2), Coordinate(-8.5, 8.7, -2.6)
        )
        s = Source(Coordinate(1.8, -2.0, 5.1), dba, 3.28, octave_band_levels=ob)
        r = Receiver(Coordinate(-8.0, -6.3, -4.9))

        # [2, -3.12, 16.6, 4.09, 4.35, 16.21, 20.37, 0.2, 'ARI'] != 0 :
        # vertical line errors
        b_old.set_start(Coordinate(-2.5, 7.7, 1.0))
        b_old.set_end(Coordinate(-2.5, 1.6, -6.5))
        b.set_start(Coordinate(-2.5, 7.7, 1.0))
        b.set_end(Coordinate(-2.5, 1.6, -6.5))
        s.set_coords(Coordinate(-6.1, 6.3, -4.6))
        r.set_coords(Coordinate(8.5, -1.6, 7.2))

        b_old.set_start(Coordinate(6.1, -3.3, -5.5))
        b_old.set_end(Coordinate(-6.5, 0.5, -6.9))
        b.set_start(Coordinate(6.1, -3.3, -5.5))
        b.set_end(Coordinate(-6.5, 0.5, -6.9))
        s.set_coords(Coordinate(1.3, -9.6, 0.7))
        r.set_coords(Coordinate(1.3, 2.0, -6.9))

        b_old_ari = b_old.get_insertion_loss_ARI(s, r)
        b_ari = b.get_insertion_loss(s, r, method="ARI")
        b_old_fres = b_old.get_insertion_loss_OB_fresnel(s, r)
        b_fres = b.get_insertion_loss(s, r, method="Fresnel")
        print(b_old_ari)
        print(b_ari)
        print(b_old_fres)
        print(b_fres)

        self.assertEqual(b_old_ari, b_ari)
        self.assertEqual(b_old_fres, b_fres)

    def parallel(self):
        """barrier and sr_line are parallel and not coincident"""
        pass

    def coincident(self):
        """barrier and sr_line are coincident -- May have different lengths"""
        # should be covered by parallel test
        pass

    def vertex_part_of_other_line(self):
        """barrier or sr_line start/end point is part of the other line"""
        pass

    def shared_vertex(self):
        """barrier and sr_line share a vertex"""
        pass


if __name__ == "__main__":
    unittest.main()

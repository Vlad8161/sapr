import sys
import unittest

from displacement.sequential import SequentialDisplacement as SeqDisp

d = [
    [0, 0, 0, 0, 3, 2, 2, 4, 2, 1],
    [0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 4, 0, 1, 0, 0, 0, 0],
    [0, 4, 4, 0, 0, 2, 2, 4, 1, 2],
    [3, 0, 0, 0, 0, 2, 2, 1, 0, 1],
    [2, 0, 1, 2, 2, 0, 2, 2, 0, 0],
    [2, 0, 0, 2, 2, 2, 0, 2, 0, 0],
    [4, 0, 0, 4, 1, 2, 2, 0, 0, 2],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 0],
]

t = [
    [0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 0, 1, 2, 3, 2, 1, 2, 3, 4],
    [1, 1, 0, 1, 2, 1, 2, 3, 2, 3],
    [1, 2, 1, 0, 1, 2, 3, 4, 3, 2],
    [2, 3, 2, 1, 0, 1, 2, 3, 2, 1],
    [2, 2, 1, 2, 1, 0, 1, 2, 1, 2],
    [2, 1, 2, 3, 2, 1, 0, 1, 2, 3],
    [3, 2, 3, 4, 3, 2, 1, 0, 1, 2],
    [3, 3, 2, 3, 2, 1, 2, 1, 0, 1],
    [3, 4, 3, 2, 1, 2, 3, 2, 1, 0],
]


class TestSequentialDisplacement(unittest.TestCase):
    def test_sequential(self):
        alg = SeqDisp(connection_matrix=d, distance_matrix=t)
        alg.compute_all()
        self.assertDictEqual(alg.map, {
            0: 0,
            1: 3,
            2: 8,
            3: 1,
            4: 2,
            5: 4,
            6: 9,
            7: 6,
            8: 5,
            9: 7,
        })


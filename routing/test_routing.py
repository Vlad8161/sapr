import sys
import unittest

from displacement.sequential import SequentialDisplacement
from main import parse_input
from routing.simple import SimpleRouting

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


schema = parse_input()
disp = SequentialDisplacement(schema['matr_d'], t)
disp.compute_all()
simple_routing = SimpleRouting(
    schema['wires_detailed'],
    disp.map,
    schema['packages']
)

while True:
    for i in simple_routing.work_field:
        print(''.join(['   ' if j == 0 else '  *' if j == -1 else ' ' + str(j) if j > 9 else '  ' + str(j) for j in i]))
    print('--------------------')
    sys.stdin.read(1)
    simple_routing.next_step()

import pytest

from structpy.graph import MapPointGraph

def test_preorder_traversal():
    mpg = MapPointGraph()
    arcs = [
        (0, 1),
        (1, 2),
        (2, 0),
        (2, 3),
        (2, 4),
        (1, 5),
        (5, 4),
        (3, 6)
    ]
    for arc in arcs:
        mpg.add(*arc)
    traversal = list(mpg.traversal_preorder(0))
    assert traversal[0] is 0
    assert traversal[1] is 1
    pos2 = traversal.index(2)
    pos5 = traversal.index(5)
    assert abs(pos2 - pos5) > 1
    assert len(traversal) == mpg.nodes_number()
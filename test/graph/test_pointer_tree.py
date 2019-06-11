import pytest

from standard.graph import PointerTree

"""
     0
  1     2
3  4   5   6
  7 8     9 10 11
"""

@pytest.fixture
def pt():
    pt = PointerTree(0)
    pt.add(0, 1)
    pt.add(0, 2)
    pt.add(1, 3)
    pt.add(1, 4)
    pt.add(2, 5)
    pt.add(2, 6)
    pt.add(4, 7)
    pt.add(4, 8)
    pt.add(6, 9)
    pt.add(6, 10)
    pt.add(6, 11)
    return pt

def test_constructor():
    pt = PointerTree(0)
    assert pt._root == 0
    assert pt.root() == 0


def test_membership(pt):
    assert pt.has_node(6)
    assert not pt.has_node(20)
    assert pt.has_arc(6, 9)
    assert not pt.has_arc(9, 6)


def test_node_finding(pt):
    a_epis = {9, 10, 11}
    for epi in pt.epis(6):
        a_epis.remove(epi)
    assert len(a_epis) == 0

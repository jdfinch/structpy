import pytest

from structpy.graph import BidictionaryTree

def test_constructor():
    bt = BidictionaryTree('a')
    assert bt._root == 'a'
    assert len(bt._nodes) == 1

"""
     0
  1     2
3  4   5   6
  7 8     9 10 11
"""

@pytest.fixture
def bt():
    t = BidictionaryTree(0)
    t.add(0, 1)
    t.add(0, 2)
    t.add(1, 3)
    t.add(1, 4)
    t.add(2, 5)
    t.add(2, 6)
    t.add(4, 7)
    t.add(4, 8)
    t.add(6, 10)
    t.add(6, 9)
    t.add(6, 11)
    return t

def test_nodes(bt):
    assert bt.parent(4) == 1
    assert bt.parent(0) == None

    children6 = {9, 10, 11}
    for epi in bt.epis(6):
        children6.remove(epi)
    assert len(children6) == 0

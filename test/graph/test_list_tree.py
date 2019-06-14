import pytest

from standard.graph import ListTree

def test_constructor():
    lt = ListTree('a')
    assert lt._root == 'a'
    assert len(lt._nodes) == 1

"""
     0
  1     2
3  4   5   6
  7 8     9 10 11
"""

@pytest.fixture
def lt():
    t = ListTree(0)
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

def test_nodes(lt):
    assert lt.parent(4) == 1
    assert lt.parent(0) == None

    children6 = {9, 10, 11}
    for epi in lt.epis(6):
        children6.remove(epi)
    assert len(children6) == 0

    found = []
    for epi in lt.epis(6):
        found.append(epi)
    assert found == [10,9,11]
    assert not found == [9,10,11]

import pytest

from standard.graph import BidictionaryGraph

def test_constructor():
    bg = BidictionaryGraph()
    assert bg._nodes == dict()
    assert bg._reverse == dict()

@pytest.fixture
def bg():
    d = BidictionaryGraph()
    d.add('a', 'b', 1)
    d.add_node('c')
    d.add_arc('a', 'c', 2)
    d.add('c', 'd', 3)
    d.add('d', 'e', 4)
    d.add('d', 'f', 2)
    d.add('f', 'c', 1)
    d.add('f', 'b', 6)
    d.add('e', 'b', 5)
    return d

def test_nodes(bg):
    fepis = {'b', 'c'}
    for epi in bg.epis('f'):
        fepis.remove(epi)
    assert len(fepis) == 0

    fpros = {'d'}
    for pro in bg.pros('f'):
        fpros.remove(pro)
    assert len(fpros) == 0

    bpros = {'a', 'f', 'e'}
    for pro in bg.pros('b'):
        bpros.remove(pro)
    assert len(bpros) == 0

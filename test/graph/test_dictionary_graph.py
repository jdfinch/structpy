import pytest

from structpy.graph import DictionaryGraph

def test_constructor():
    dg = DictionaryGraph()
    assert dg._nodes == dict()

@pytest.fixture
def dg():
    d = DictionaryGraph()
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

def test_nodes(dg):

    assert dg.has_node('e')
    assert not dg.has_node('z')
    assert dg.nodes_number() == 6

    fepis = {'b', 'c'}
    for epi in dg.epis('f'):
        fepis.remove(epi)
    assert len(fepis) == 0

    farcs = {6, 1}
    for arc in dg.arcs_out('f'):
        farcs.remove(arc)
    assert len(farcs) == 0
import pytest

from standard.graph import ListGraph

def test_constructor():
    lg = ListGraph()
    assert lg._nodes == dict()
    assert lg._reverse == dict()


@pytest.fixture
def dg():
    d = ListGraph()
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

@pytest.fixture
def bg():
    d = ListGraph()
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

def test_nodes_bi(bg):
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

    assert bg.arc('f','b') == 6

    found = []
    for arc in bg.arcs_out('f'):
        found.append(arc)
    assert found == [1,6]
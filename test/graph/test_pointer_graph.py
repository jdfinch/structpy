import pytest

from standard.graph import PointerGraph

def test_constructor():
    pg = PointerGraph()

@pytest.fixture
def pg():
    pg = PointerGraph()
    pg.add_node('a')
    pg.add_node('b')
    pg.add_arc('a', 'b')
    pg.add('a', 'c')
    pg.add('c', 'd')
    pg.add('d', 'e')
    pg.add('d', 'f')
    pg.add('f', 'c')
    pg.add('f', 'b')
    pg.add('e', 'b')
    return pg

def test_membership(pg):
    assert pg.has_node('a')
    assert not pg.has_node('z')
    assert pg.has_arc('d', 'f')
    assert not pg.has_arc('c', 'a')

def test_node_finding(pg):
    a_epis = {'c', 'b'}
    for epi in pg.epis('a'):
        a_epis.remove(epi)
    assert len(a_epis) == 0
    b_pros = {'a', 'f', 'e'}
    for pro in pg.pros('b'):
        b_pros.remove(pro)
    assert len(b_pros) == 0

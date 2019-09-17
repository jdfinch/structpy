import pytest

from structpy.graph import MultiFlexGraph

@pytest.fixture
def mfg():
    g = MultiFlexGraph()
    arcs = [
        (1, 2, 'a'),
        (1, 3, 'a'),
        (1, 4, 'a'),
        (4, 9, 'b'),
        (9, 1, 'b')
    ]
    for arc in arcs:
        g.add(*arc)
    return g

def test_constructor(mfg):
    assert mfg.nodes_number() == 5
    assert mfg.arcs_number() == 5
    assert mfg.arc(1, 2) == {'a'}
    assert set(mfg.epis(1, 'a')) == {2, 3, 4}

def test_multi_add(mfg):
    mfg.add(1, 2, 'b')
    assert set(mfg.epis(1, 'a')) == {2, 3, 4}
    assert set(mfg.epis(1, 'b')) == {2}
    assert mfg.arcs_number() == 6
    assert mfg.nodes_number() == 5
    assert set(mfg.arcs_between(1, 2)) == {'a', 'b'}
    assert mfg.arc(1, 2) == {'a', 'b'}

def test_multi_remove(mfg):
    mfg.add(1, 2, 'b')
    mfg.remove(1, 2, 'a')
    assert mfg.arcs_number() == 5
    assert mfg.nodes_number() == 5
    assert set(mfg.arcs_between(1, 2)) == {'b'}
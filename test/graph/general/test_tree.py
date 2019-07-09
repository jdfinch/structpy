import pytest

from structpy.graph import FlexTree


types = [FlexTree]

@pytest.mark.parametrize('cls', types)
def test_constructor(cls):
    ft = cls(0)
    assert ft.root() == 0

@pytest.mark.parametrize('cls', types)
def test_add_membership(cls):
    ft = cls(0)
    assert ft.root() == 0
    ft.add(0, 1)
    assert ft.has_node(0)
    assert ft.has_arc(0, 1)
    ft.add(0, 2)
    assert ft.has_node(2)
    assert ft.has_arc(0, 2)
    ft.add(1, 3)
    assert ft.has_node(3)
    assert ft.has_arc(1, 3)

@pytest.fixture(params=types)
def mpg(request):
    cls = request.param
    g = cls(0)
    arcs = [
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 6),
        (6, 7),
        (6, 8)
    ]
    for arc in arcs:
        g.add(*arc)
    return g

def test_nodes(mpg):
    nodes = set(range(9))
    for node in mpg.nodes():
        nodes.remove(node)
    assert len(nodes) == 0

def test_arcs(mpg):
    arcs = {
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 6),
        (6, 7),
        (6, 8)
    }
    for arc in mpg.arcs():
        if len(arc) == 3:
            arc = (arc[0], arc[1])
        arcs.remove(arc)
    assert len(arcs) == 0

def test_has(mpg):
    assert mpg.has(0)
    assert not mpg.has(-1)
    assert mpg.has(0, 1)
    assert not mpg.has(1, 0)

def test_number(mpg):
    assert mpg.nodes_number() == 9
    assert mpg.arcs_number() == 8

def test_epis(mpg):
    epis1 = {3, 4, 5}
    for epi in mpg.epis(1):
        epis1.remove(epi)
    assert len(epis1) == 0

def test_parent(mpg):
    assert mpg.pros_number(1) == 1
    assert mpg.pros_number(5) == 1
    assert mpg.parent(5) == 1
    assert mpg.parent(0) is None
    assert mpg.parent(7) == 6

def test_epis_number(mpg):
    assert mpg.epis_number(1) == 3

def test_destruction(mpg):
    mpg.remove_node(8)
    assert not mpg.has_node(8)
    assert mpg.epis_number(6) == 1

def test_replace_node(mpg):
    mpg.replace_node(2, 9)
    assert mpg.has_node(9)
    assert not mpg.has_node(2)
    assert mpg.has_arc(0, 9)
    assert mpg.has_arc(9, 6)
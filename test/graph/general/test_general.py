import pytest

from structpy.graph import FlexGraph, MapPointGraph


types = [MapPointGraph, FlexGraph]

@pytest.mark.parametrize('cls', types)
def test_constructor(cls):
    mpg = cls()

@pytest.mark.parametrize('cls', types)
def test_add_membership(cls):
    mpg = cls()
    mpg.add_node(0)
    assert mpg.has_node(0)
    assert not mpg.has_node(-1)
    mpg.add_node(1)
    mpg.add_arc(0, 1)
    assert mpg.has_arc(0, 1)
    assert not mpg.has_arc(1, 0)
    mpg.add(2, 0)
    assert mpg.has_node(2)
    assert mpg.has_arc(2, 0)
    assert not mpg.has_arc(0, 2)
    assert mpg.has_arc(0, 1)
    mpg.add(2, 3)
    assert mpg.has_arc(2, 0)
    assert mpg.has_arc(2, 3)
    assert not mpg.has_arc(1, 3)
    assert mpg.has_node(3)

@pytest.fixture(params=types)
def mpg(request):
    cls = request.param
    g = cls()
    arcs = [
        (0, 1),
        (1, 2),
        (2, 0),
        (2, 3),
        (2, 4),
        (1, 5),
        (5, 4),
        (4, 2),
        (3, 6)
    ]
    for arc in arcs:
        g.add(*arc)
    return g

def test_nodes(mpg):
    nodes = set(range(7))
    for node in mpg.nodes():
        nodes.remove(node)
    assert len(nodes) == 0

def test_arcs(mpg):
    arcs = {
        (0, 1),
        (1, 2),
        (2, 0),
        (2, 3),
        (2, 4),
        (1, 5),
        (5, 4),
        (4, 2),
        (3, 6)
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
    assert mpg.nodes_number() == 7
    assert mpg.arcs_number() == 9


def test_epis(mpg):
    epis2 = {0, 3, 4}
    for epi in mpg.epis(2):
        epis2.remove(epi)
    assert len(epis2) == 0


def test_pros(mpg):
    pros4 = {2, 5}
    for pro in mpg.pros(4):
        pros4.remove(pro)
    assert len(pros4) == 0


def test_pros_epis_number(mpg):
    assert mpg.epis_number(2) == 3
    assert mpg.pros_number(4) == 2

def test_destruction(mpg):
    assert mpg.has_arc(1, 2)
    mpg.remove_arc(1, 2)
    assert not mpg.has_arc(1, 2)
    assert mpg.has_node(1)
    assert mpg.has_node(2)
    mpg.remove_node(1)
    assert not mpg.has_node(1)
    assert not mpg.has_arc(0, 1)
    assert mpg.has_node(0)
    mpg.remove(4)
    assert not mpg.has_node(4)
    assert not mpg.has_arc(5, 4)
    assert not mpg.has_arc(2, 4)
    assert not mpg.has_arc(4, 2)
    mpg.remove(2, 0)
    assert mpg.has_node(0)
    assert mpg.has_node(0)
    assert not mpg.has_arc(2, 0)

def test_replace_node(mpg):
    mpg.replace_node(2, 9)
    assert mpg.has_node(9)
    assert not mpg.has_node(2)
    assert mpg.has_arc(9, 0)
    assert mpg.has_arc(4, 9)
    assert mpg.has_arc(9, 3)

def test_replace_pro_epi(mpg):
    mpg.replace_pro(0, 1, 2)
    assert not mpg.has_arc(0, 1)
    assert mpg.has_arc(2, 1)
    assert mpg.has_node(0)
    mpg.replace_epi(2, 3, 6)
    assert not mpg.has_arc(2, 3)
    assert mpg.has_arc(2, 6)
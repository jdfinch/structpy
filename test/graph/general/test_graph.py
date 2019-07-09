import pytest, os

from structpy.graph import FlexGraph, MapPointGraph

types=[MapPointGraph,FlexGraph]

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

@pytest.fixture(params=[FlexGraph])
def g(request):
    cls = request.param
    g = cls().load(os.path.join(os.getcwd(),'test','graph','general','example'))
    return g

def test_load(g):
    assert g.has_node('sport')
    assert g.has_node('soccer')
    assert g.has_node('harry potter (character)')
    assert g.has_node('ron weasley')
    assert g.has_node('character')

    assert g.has_arc('soccer','sport')
    assert g.has_arc('soccer','activity')
    assert g.has_arc('ron weasley', 'harry potter (character)')
    assert g.has_arc('character', 'ron weasley')

    assert list(g.epis('harry potter (character)')) == ['character','ron weasley']
    assert list(g.epis('sport')) == ['soccer','basketball']
    assert list(g.arcs_out('harry potter (character)')) == ['is a','friends']

def test_save(g):
    file = os.path.join(os.getcwd(),
                        'test',
                        'graph',
                        'general',
                        'saved_example')
    g.save(file)
    nodes = list(g.nodes())
    for node in nodes:
        g.remove(node)
    assert len(list(g.nodes())) == 0
    assert len(list(g.arcs())) == 0
    g.load(file)
    assert len(list(g.nodes())) > 0
    assert len(list(g.arcs())) > 0
    test_load(g)

@pytest.fixture(params=[MapPointGraph])
def mpg_example(request):
    cls = request.param
    mpg_example = cls().load(os.path.join(os.getcwd(),'test','graph','general','example_mpg'))
    return mpg_example

def test_load_mpg(mpg_example):
    assert sorted(list(mpg_example.nodes())) == \
           sorted(['colors','blue','green','red','names','jane','bob','professions','programmer'])

    for node in mpg_example.nodes():
        if node == 'colors':
            assert sorted(list(mpg_example.epis(node))) == sorted(['blue','red','green'])
        elif node == 'professions':
            assert list(mpg_example.epis(node)) == ['programmer']
        elif node == 'names':
            assert sorted(list(mpg_example.epis(node))) == sorted(['jane','bob'])

    assert mpg_example.has_arc('colors','red')
    assert mpg_example.has_arc('names', 'bob')

def test_save(mpg_example):
    file = os.path.join(os.getcwd(),
                        'test',
                        'graph',
                        'general',
                        'saved_example_mpg')
    mpg_example.save(file)
    nodes = list(mpg_example.nodes())
    for node in nodes:
        mpg_example.remove(node)
    assert len(list(mpg_example.nodes())) == 0
    assert len(list(mpg_example.arcs())) == 0
    mpg_example.load(file)
    assert len(list(mpg_example.nodes())) > 0
    assert len(list(mpg_example.arcs())) > 0
    test_load_mpg(mpg_example)

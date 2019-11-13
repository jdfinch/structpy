
import pytest

from structpy.graph.traversal import Traversal, rings
from structpy.graph.traversal.frontier import Stack, Queue, Memoried, DepthBounded
from structpy.graph.labeled_digraph import MapDigraph

@pytest.fixture()
def graph():
    n = MapDigraph()
    n.add_node(1)
    n.add_node(2)
    n.add_node(3)
    n.add_node(4)
    n.add_node(5)
    n.add_arc(1, 2, 'a')
    n.add_arc(1, 3, 'a')
    n.add_arc(2, 3, 'b')
    n.add_arc(2, 1, 'c')
    n.add_arc(2, 4, 'd')
    n.add_arc(4, 1, 'e')
    n.add_arc(4, 5, 'f')
    n.add_arc(5, 3, 'e')
    return n

ordering = [
    (1, 2),
    (1, 3),
    (2, 4),
    (4, 5)
]

ring_sets = [
    {(None, 1, None)},
    {(1, 2, 'a'), (1, 3, 'a')},
    {(2, 4, 'd')},
    {(4, 5, 'f')}
]

def test_breadth_first_traversal(graph):
    traversal = list(Traversal(graph, Queue()).memoried().start(1))
    assert len(traversal) == graph.len_nodes()
    for a, b in ordering:
        assert traversal.index(a) < traversal.index(b)

def test_breadth_first_arc_traversal(graph):
    traversal = list(Traversal(graph, Queue()).arcs().memoried().start(1))
    assert len(traversal) == len(ordering)
    for arc in ordering:
        assert arc in traversal

def test_breadth_first_labeled_arc_traversal(graph):
    traversal = list(Traversal(graph, Queue()).labeled_arcs().memoried().start(1))
    assert len(traversal) == len(ordering)
    arcs = [(source, target) for source, target, label in traversal]
    for arc in ordering:
        assert arc in arcs

def test_breadth_first_bounded_traversal(graph):
    traversal = list(Traversal(graph, Queue()).memoried().to_depth(2).start(1))
    assert len(traversal) == graph.len_nodes() - 1
    for a, b in ordering[:-1]:
        assert traversal.index(a) < traversal.index(b)

def test_ring_traversal(graph):
    i = 0
    traversal = Traversal(graph, Queue()).memoried().with_depth().start(1)
    for ring in rings(traversal):
        r = set(ring)
        t = {x[1] for x in ring_sets[i]}
        assert r == t
        i += 1
    assert i == len(ring_sets)

def test_ring_arc_traversal(graph):
    i = 1
    traversal = Traversal(graph, Queue()).arcs().memoried().with_depth().start(1)
    for ring in rings(traversal):
        ring = set(ring)
        assert ring == {(source, target) for source, target, _ in ring_sets[i]}
        i += 1

def test_ring_labeled_arc_traversal(graph):
    i = 1
    traversal = Traversal(graph, Queue()).labeled_arcs().memoried().with_depth().start(1)
    for ring in rings(traversal):
        ring = set(ring)
        assert ring == ring_sets[i]
        i += 1



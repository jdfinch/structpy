
import pytest

from structpy.graph.traversal.traversal import \
    _Traversal as Traversal, _TraversalStep as Step
from structpy.graph.traversal.frontier import Stack, Queue, MemFrontier
from structpy.graph.traversal import BreadthFirstTraversal, RingTraversal
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
    (2, 3),
    (2, 4),
    (4, 5)
]

rings = [
    {(None, 1, None)},
    {(1, 2, 'a'), (1, 3, 'a')},
    {(2, 4, 'd')},
    {(4, 5, 'f')}
]

def test_breadth_first_traversal(graph):
    traversal = list(Traversal(graph, MemFrontier(Queue(Step, 1))))  #list(BreadthFirstTraversal(graph, 1))
    assert len(traversal) == graph.len_nodes()
    for a, b in ordering:
        assert traversal.index(a) < traversal.index(b)

def test_breadth_first_arc_traversal(graph):
    traversal = list(BreadthFirstTraversal.arcs(graph, 1))
    assert len(traversal) == graph.len_nodes()
    for arc in ordering:
        assert arc in traversal

def test_breadth_first_labeled_arc_traversal(graph):
    traversal = list(BreadthFirstTraversal.labeled_arcs(graph, 1))
    assert len(traversal) == graph.len_nodes()
    arcs = [(source, target) for source, target, label in traversal]
    for arc in ordering:
        assert arc in arcs

def test_breadth_first_bounded_traversal(graph):
    traversal = list(BreadthFirstTraversal.bounded(graph, 1, 2))
    assert len(traversal) == graph.len_nodes() - 1
    for a, b in ordering[:-1]:
        assert traversal.index(a) < traversal.index(b)

def test_ring_traversal(graph):
    i = 0
    for ring in RingTraversal(graph, 1):
        assert set(ring) == {x[1] for x in rings[i]}
        i += 1
    assert i == len(rings)

def test_ring_arc_traversal(graph):
    i = 1
    for ring in RingTraversal.arcs(graph, 1):
        ring = set(ring)
        assert ring == {(source, target) for source, target, _ in rings[i]}
        i += 1

def test_ring_labeled_arc_traversal(graph):
    i = 1
    for ring in RingTraversal.labeled_arcs(graph, 1):
        ring = set(ring)
        assert ring == rings[i]
        i += 1



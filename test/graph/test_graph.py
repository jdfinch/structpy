import pytest

from standard.graph import Graph
from standard.graph.frontiers import SearchTree

g = None

def test_inheritence_nodebased():
    """Test inheritence and constructor"""

    class MyGraph(Graph):    
        def __init__(self):
            self._nodes = {}
        def add_node(self, node):
            if node not in self._nodes:
                self._nodes[node] = {}
        def add_arc(self, pro, epi, arc=None):
            self._nodes[pro][epi] = arc
        def arc(self, pro, epi):
            if pro in self._nodes and epi in self._nodes[pro]:
                return self._nodes[pro][epi]

    global g
    g = MyGraph()

def test_add():
    """Test add methods (add, add_node, add_arc)"""
    g.add('a', 'b', 1)
    g.add('c')
    g.add_arc('a', 'c', 2)
    g.add_node('d')
    g.add_arc('c', 'd', 3)
    g.add('d', 'e', 4)
    g.add('d', 'f', 2)
    g.add_arc('f', 'c', 1)
    g.add('f', 'b', 6)
    g.add('e', 'b', 5)

def test_membership():
    """Test node and arc membership (has, has_node, has_arc)"""
    assert g.has_node('a')
    assert g.has('e')
    assert not g.has('y')
    assert not g.has_node('x')
    assert g.has_arc_value(4)
    assert not g.has_arc_value(9)
    assert g.has('a', 'b')
    assert g.has_arc('f', 'b')
    assert not g.has('a', 'd')
    assert not g.has('c', 'a')

def test_iteration_methods():
    """Test iteration (nodes, arcs)"""
    nodes = set('abcdef')
    arcs = list(range(1, 7)) + [1, 2]
    for node in g.nodes():
        nodes.remove(node)
    for arc in g.arcs():
        arcs.remove(arc)
    assert len(nodes) == 0
    assert len(arcs) == 0

def test_node_adjacency_iterators():
    """Test nodes adjacent to certain node (pros, epis)"""
    nodes = set('bc')
    for node in g.epis('a'):
        nodes.remove(node)
    assert len(nodes) == 0
    assert len(list(g.pros('a'))) == 0
    nodes = set('ef')
    for node in g.epis('d'):
        nodes.remove(node)
    assert len(nodes) == 0
    for node in g.pros('d'):
        assert node == 'c'

def test_node_arc_adjacency():
    """Test nodes adjacent to an arc (pro, epi)"""
    assert g.pro(3) == 'c'
    assert g.epi(3) == 'd'
    assert g.pro(1) == 'a' or g.pro(1) == 'f'
    assert g.epi(1) == 'b' or g.epi(1) == 'c'
    assert g.pro(2) != 'e'
    assert g.epi(2) != 'e'

def test_arc_node_adjacency():
    """Test arcs adjacent to certain node(s) (arcs_in, arcs_out, arc)"""
    assert g.arc('a', 'c') == 2
    assert g.arc('f', 'c') == 1
    assert g.arc('d', 'f') == 2
    assert g.arc('e', 'a') is None
    assert g.arc('b', 'a') is None
    arcs = [1, 6]
    for arc in g.arcs_out('f'):
        arcs.remove(arc)
    assert len(arcs) == 0
    arcs = [1, 5, 6]
    for arc in g.arcs_in('b'):
        arcs.remove(arc)
    assert len(arcs) == 0
    assert len(list(g.arcs_out('b'))) == 0

def test_traversal():
    from standard.graph.frontiers import MemQueue as BreadthFirst, \
        MemStack as DepthFirst
    def before(ls, a, b):
        i = ls.index(a)
        j = ls.index(b)
        return i < j
    assert before([2, 4, 6], 2, 6)
    assert not before([2, 4, 6], 4, 2)
    
    traversal = list(g.traverse(BreadthFirst(), 'f'))
    assert len(traversal) == len(set(traversal))
    assert len(traversal) == 5
    assert before(traversal, 'f', 'b')
    assert before(traversal, 'b', 'd')
    assert before(traversal, 'c', 'e')
    assert before(traversal, 'd', 'e')
    assert before(traversal, 'b', 'e')
    assert not before(traversal, 'd', 'c')

    traversal = list(g.traverse(DepthFirst(), 'f'))
    assert len(traversal) == len(set(traversal))
    assert len(traversal) == 5
    assert before(traversal, 'f', 'b')
    assert before(traversal, 'c', 'e')
    assert before(traversal, 'd', 'e')
    assert not before(traversal, 'd', 'c')

'''
def test_search():
    st = SearchTree('a', 'f')
    assert list(g.search(st)) == ['a', 'c', 'd', 'f'] 
    assert list(g.search_reverse(SearchTree('f', 'a'))) == ['f', 'd', 'c', 'a']
'''

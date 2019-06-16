import pytest

from standard.graph.frontiers import PrioritySearchTree
from standard.graph import Graph
from standard.graph.frontiers import SearchTree

def priority_function(pro, epi, arc):
    if pro is None or arc is None:
        return 1
    else:
        return arc

def aggregation_function(p1, p2):
    return p1 * p2

def test_constructor():
    st = PrioritySearchTree('a', 'f', priority_function, aggregation_function)
    assert st._root == 'a'
    assert st._target == 'f'
    assert st._active == 'a'
    
def test_priority_queue1():
    st = PrioritySearchTree('a', 'x', priority_function, aggregation_function)
    st.add('a', 'b', 0.5)
    st.add('a', 'c', 0.4)
    assert st.pop().split('_')[0] == 'b'
    st.add('b', 'd', 0.3)
    assert st.pop().split('_')[0] == 'c'
    st.add('c', 'd', 0.9)
    st.add('c', 'b', 0.2)
    assert st.pop().split('_')[0] == 'd'
    st.add('d', 'e', 0.1)
    st.add('d', 'x', 0.4)
    assert st.pop().split('_')[0] == 'x'

def test_priority_queue2():
    st = PrioritySearchTree('c', 'e', priority_function, aggregation_function)
    st.add('c', 'b', 0.2)
    st.add('c', 'd', 0.9)
    assert st.pop() == 'd'
    st.add('d', 'e', 0.1)
    st.add('d', 'x', 0.4)
    assert st.pop() == 'x'
    assert st.pop() == 'b'
    st.add('b', 'd', 0.3)
    assert st.pop() == 'e'

g = None

def test_graph():

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
    g.add('a','b',0.5)
    g.add('a','c',0.4)
    g.add('c','b',0.2)
    g.add('c','d',0.9)
    g.add('b','d',0.3)
    g.add('d','e',0.1)
    g.add('d','x',0.4)
    g.add('e','x',0.1)

def test_search():
    pst = PrioritySearchTree('a', 'x', priority_function, aggregation_function)
    assert list(g.search(pst)) == ['a','c','d','x']
    pst = PrioritySearchTree('c', 'e', priority_function, aggregation_function)
    assert list(g.search(pst)) == ['c','d','e']



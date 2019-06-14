import pytest

from standard.graph.frontiers import PrioritySearchTree

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
    
def test_priority_queue():
    st = PrioritySearchTree('a', 'x', priority_function, aggregation_function)
    st.add('a', 'b', 0.5)
    st.add('a', 'c', 0.4)
    assert st.pop() == 'b'
    st.add('b', 'd', 0.3)
    assert st.pop() == 'd'
    st.add('d', 'e', 0.1)
    st.add('d', 'x', 0.4)
    assert st.pop() == 'c'
    st.add('c', 'd', 0.9)
    st.add('c', 'b', 0.2)
    assert st.pop() == 'x'
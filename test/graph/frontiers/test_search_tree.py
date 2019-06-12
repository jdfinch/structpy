import pytest

from standard.graph.frontiers import SearchTree

def test_constructor():
    st = SearchTree('a', 'f')
    assert st._target == 'f'
    assert st._root == 'a'
    assert st._complete == False

def test_search():
    st = SearchTree('a', 'f')
    assert st.pop() == 'a'
    st.add('b')
    st.add('c')
    assert st.pop() == 'b'
    assert st.pop() == 'c'
    st.add('d')
    assert st.pop() == 'd'
    st.add('d', 'e')
    assert not st.complete()
    st.add('d', 'f')
    assert st.complete()
    assert st.pop() == 'e'
    assert list(st.result()) == ['a', 'c', 'd', 'f']

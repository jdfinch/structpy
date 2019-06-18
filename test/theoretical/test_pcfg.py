import pytest

from standard.theoretical import Pcfg
from standard.graph.frontiers import PrioritySearchTree
from standard.graph.linked_tree import LinkedTree
from standard.graph.linked_graph import Node

gramstring = '''\
S -> NP VP 1.0
NP -> N 0.2 | DET N 0.8
VP -> V 0.15 | V PP 0.25 | V NP 0.35 | V NP PP 0.25
PP -> PREP NP 1.0
N -> dog 0.2 | cat 0.5 | bone 0.1 | catnip 0.2
V -> runs 0.3 | screams 0.2 | likes 0.5
DET -> the 1.0
PREP -> on 0.4 | in 0.6\
'''

def test_constructor():
    dm = Pcfg()

def test_from_string():
    sm = Pcfg.from_string(gramstring)
    assert sm.has_arc('S', 'S0')
    assert sm.has_arc('S0', 'NP')
    assert sm.has_arc('S0', 'VP')
    assert sm.has_node('NP')
    assert sm.has_arc('NP', 'NP0')
    assert sm.has_arc('NP', 'NP1')
    assert not sm.has_arc('NP', 'NP2')

    assert sm.arc('NP', 'NP0') == 0.2
    assert sm.arc('NP', 'NP1') == 0.8
    assert sm.has_node('NP1')
    assert sm.has_arc('NP1', 'DET')
    assert sm.arc('NP1', 'DET') == 0
    assert sm.has_arc('NP1', 'N')
    assert sm.arc('NP1', 'N') == 1

def priority_function(pro, epi, arc):
    if pro is None or arc is None:
        return 1
    else:
        return arc

def aggregation_function(p1, p2):
    return p1 * p2

def test_reverse_search():
    sm = Pcfg.from_string(gramstring)

    pst = PrioritySearchTree('NP', 'S', priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['NP', 'S0', 'S']

    pst = PrioritySearchTree('N', 'S', priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['N', 'NP0', 'NP', 'S0', 'S']

    pst = PrioritySearchTree('the', 'S', priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['the', 'DET0', 'DET', 'NP1', 'NP', 'S0', 'S']

    pst = PrioritySearchTree('runs', 'VP', priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['runs', 'V0', 'V', 'VP2', 'VP']

    pst = PrioritySearchTree('N', 'NP', priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['N', 'NP0', 'NP']

def test_completion_check():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')


    pt = LinkedTree()
    pt.add(s0,np1)
    pt.add(np1,det0)
    pt.add(det0,the)

    assert pt.is_complete(np0, sm) is None
    assert pt.is_complete(np1, sm) is False

def test_building_parse_tree_using_linked_tree():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = LinkedTree()
    pt.add(s0, np1)
    pt.add(np1, det0)
    pt.add(det0, the)

    n0 = Node('N0')
    dog = Node('dog')

    pt.add(np1,n0)
    pt.add(n0,dog)

    assert pt.is_complete(np1, sm) is True

    pt.add(s0,'VP2')

    assert [x.get_value() for x in pt.epis(s0)] == ['NP1','VP2']

    vp2 = pt.get_node(s0,'VP2')
    assert vp2.get_value() == 'VP2'
    assert pt.has_arc(s0,vp2)

    pt.add(vp2,'V2')
    pt.add(pt.get_node(vp2,'V2'),'likes')

    assert [x.get_value() for x in pt.epis(vp2)] == ['V2']

    assert pt.is_complete(vp2,sm) is False

    pt.add(vp2,'NP1')

    assert pt.is_complete(np1, sm) is True
    assert pt.is_complete(pt.get_node(vp2,'NP1'),sm) is False

    det0_2 = Node('DET0')
    the_2 = Node('the')
    n2 = Node('N2')
    bone = Node('bone')

    pt.add(pt.get_node(vp2,'NP1'),det0_2)
    pt.add(det0_2,the_2)

    parent = pt.get_node(vp2,'NP1')
    pt.add(parent,n2)
    pt.add(n2,bone)

    assert [x.get_value() for x in pt.epis(parent)] == ['DET0','N2']
    assert pt.is_complete(parent,sm)


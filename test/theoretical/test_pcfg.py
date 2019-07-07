import pytest

from structpy.theoretical import Pcfg
from structpy.graph.frontiers import PrioritySearchTree

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
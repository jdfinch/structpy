from standard.theoretical.pcfg_parse_tree import PcfgParseTree
from standard.graph.node_graph import Node
from standard.theoretical.pcfg import Pcfg, NodeType
from standard.graph.frontiers import PrioritySearchTree

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

def test_completion_check():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = PcfgParseTree(s0)
    pt.add(s0,np1)
    pt.add(np1,det0)
    pt.add(det0,the)

    assert pt.is_complete(np0, sm) is None
    assert pt.is_complete(np1, sm) is False

def test_building_parse_tree_using_node_tree():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = PcfgParseTree(s0)
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

def test_get_next():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = PcfgParseTree(s0)
    pt.add(s0, np1)
    pt.add(np1, det0)
    pt.add(det0, the)

    assert pt.next_child(np1, sm) == 'N'

    n0 = Node('N0')
    dog = Node('dog')

    pt.add(np1, n0)
    pt.add(n0, dog)

    assert pt.next_child(s0, sm) == 'VP'

    vp2 = Node('VP2')
    v2 = Node('V2')
    likes = Node('likes')

    pt.add(s0,vp2)
    pt.add(vp2,v2)
    pt.add(v2,likes)

    assert pt.next_child(vp2, sm) == 'NP'

def test_get_next_from_parse_tree():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = PcfgParseTree(s0)
    pt.add(s0, np1)
    pt.add(np1, det0)
    pt.add(det0, the)

    parent,child = pt.get_next(sm)
    assert parent.get_value() == 'NP1'
    assert child == 'N'

    n0 = Node('N0')
    dog = Node('dog')

    pt.add(np1, n0)
    pt.add(n0, dog)

    parent, child = pt.get_next(sm)
    assert parent.get_value() == 'S0'
    assert child == 'VP'

    vp2 = Node('VP2')
    v2 = Node('V2')
    likes = Node('likes')

    pt.add(s0, vp2)
    pt.add(vp2, v2)
    pt.add(v2, likes)

    parent, child = pt.get_next(sm)
    assert parent.get_value() == 'VP2'
    assert child == 'NP'

    np1_2 = Node('NP1')
    det0_2 = Node('DET0')
    the_2 = Node('the')
    n2 = Node('N2')
    bone = Node('bone')

    pt.add(vp2,np1_2)
    pt.add(np1_2, det0_2)
    pt.add(det0_2, the_2)

    parent, child = pt.get_next(sm)
    assert parent.get_value() == 'NP1'
    assert child == 'N'

    pt.add(np1_2, n2)
    pt.add(n2, bone)

    parent, child = pt.get_next(sm)
    assert parent is None
    assert child is None

def priority_function(pro, epi, arc):
    if pro is None or arc is None:
        return 1
    else:
        return arc

def aggregation_function(p1, p2):
    return p1 * p2

def test_parsing():
    sm = Pcfg.from_string(gramstring)

    s0 = Node('S0')
    np0 = Node('NP0')
    np1 = Node('NP1')
    det0 = Node('DET0')
    the = Node('the')

    pt = PcfgParseTree(s0)
    pt.add(s0, np1)
    pt.add(np1, det0)
    pt.add(det0, the)

    parent,target = pt.get_next(sm)
    source = 'dog'

    pst = PrioritySearchTree(source, target, priority_function, aggregation_function)
    assert list(sm.search_reverse(pst)) == ['dog','N0','N']

    pt.add_branch(parent,sm.to_reverse_parse_path(sm.search_reverse(pst)))

    assert [x.get_value() for x in pt.epis(parent)] == ['DET0','N0']
    assert [x.get_value() for x in pt.epis(pt.get_node(parent,'N0'))] == ['dog']


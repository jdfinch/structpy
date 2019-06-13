import pytest

from standard.theoretical.pcfg import _Node
from standard.theoretical import Pcfg

gramstring = '''\
S -> NP VP 1.0
NP -> N 0.2 | DET N 0.8
VP -> V 0.15 | V PP 0.25 | V NP 0.35 | V NP PP 0.25
PP -> PREP NP 1.0
N -> dog 0.2 | cat 0.5 | bone 0.1 | catnip 0.2
V -> run 0.3 | scream 0.2 | like 0.5
PREP -> on 0.4 | in 0.6\
'''

def test_constructor():
    dm = Pcfg()

def test_from_string():
    sm = Pcfg.from_string(gramstring)
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


import pytest
from structpy.collection import Bidictionary

def test_constructor():
    bd = Bidictionary()
    bd2 = Bidictionary({'k': 'v', 'k2': 'v2'})
    assert bd2 == {'k': 'v', 'k2': 'v2'}

def test_bidirection_add():
    bd = Bidictionary()
    bd['a'] = 1
    bd['b'] = 2
    assert bd['a'] == 1
    assert bd['b'] == 2
    assert bd.reverse()[1] == 'a'
    assert bd.reverse()[2] == 'b'

def test_bidirection_del():
    bd = Bidictionary()
    bd['a'] = 1
    bd['b'] = 2
    del bd['a']
    assert len(bd.reverse()) == 1
    assert bd.reverse()[2] == 'b'
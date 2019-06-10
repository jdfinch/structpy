import pytest

import os
print(os.getcwd())

from standard.graph.frontiers import MemQueue
from standard.graph.frontiers import MemStack
from standard.graph.frontiers import Queue, Stack

def test_constructor():
    mq = MemQueue([1, 2, 3])
    ms = MemStack((1, 2 ,3))

def test_eq():
    mq = MemQueue([1, 2, 3])
    assert mq == MemQueue([1, 2, 3])
    assert mq == Queue((1, 2, 3))
    assert mq != MemQueue([2, 1, 3 , 4])
    assert mq != MemQueue([2, 1, 3])
    ms = MemStack([1, 2, 3])
    assert ms == MemStack([1, 2, 3])
    assert ms == Stack((1, 2, 3))
    assert ms != MemStack([2, 1, 3, 4])
    assert ms != MemStack([2, 1, 3])

def test_add():
    mq = MemQueue([1, 2, 3])
    mq.add(5)
    assert mq == MemQueue((1, 2, 3, 5))
    mq.add(4)
    assert mq == MemQueue((1, 2, 3, 5, 4))
    # test the "memoried" part of MemQueue
    mq.add(4)
    print('mq:', mq)
    assert mq == MemQueue((1, 2, 3, 5, 4))
    mq.add(2)
    assert mq == MemQueue((1, 2, 3, 5, 4))
    ms = MemStack([1, 2, 3])
    ms.add(5)
    assert ms == MemStack((1, 2, 3, 5))
    ms.add(4)
    assert ms == MemStack((1, 2, 3, 5, 4))
    # test the "memoried" part of MemStack
    ms.add(2)
    assert ms == MemStack((1, 2, 3, 5, 4))
    ms.add(4)
    assert ms == MemStack((1, 2, 3, 5, 4))

def test_pop():
    mq = MemQueue([1, 2, 3])
    assert mq.pop() == 1
    assert mq.nodes_number() == 2
    ms = MemStack([1, 2, 3])
    assert ms.pop() == 3
    assert ms.nodes_number() == 2
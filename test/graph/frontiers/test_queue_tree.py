import pytest

from standard.graph.frontiers import QueueTree, Queue

def test_constructor():
    qt = QueueTree('a')
    qt2 = QueueTree('a', (1, 2, 3))
    assert qt.root() == 'a'
    assert qt2.queue() == Queue((1, 2, 3))

def test_add():
    qt = QueueTree('a')

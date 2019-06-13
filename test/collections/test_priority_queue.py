import pytest

from standard.collections import PriorityQueue

def test_priority_queue():
    pq = PriorityQueue((3, 1, 2))
    assert pq == [1, 2, 3]
    pq.add(2.5)
    assert pq == [1, 2, 2.5, 3]
    assert pq.pop() == 3

"""
Defines a potentially infinite sequence of values that can be iterated
over, where each value is derived from an update of the previous one.

Test.
"""

from structpy.collection.enumerable.finite_markov_enumerable import FiniteMarkovEnumerableSpec
from structpy.collection.enumerable.infinite_markov_enumerable import InfiniteMarkovEnumerableSpec, InfiniteMarkovEnumerable

def MyFunction():
    """this is a function"""
    return 2

__all__ = [
    'FiniteMarkovEnumerableSpec',
    'InfiniteMarkovEnumerableSpec',
    'InfiniteMarkovEnumerable',
    'MyFunction'
]

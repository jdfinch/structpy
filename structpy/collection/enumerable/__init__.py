
"""
Defines a potentially infinite sequence of values that can be iterated
over, where each value is derived from an update of the previous one.

Test.
"""

from structpy.collection.enumerable.finite_markov_enumerable import FiniteMarkovEnumerableSpec as FMES
from structpy.collection.enumerable.infinite_markov_enumerable import InfiniteMarkovEnumerableSpec as IMES
from structpy.collection.enumerable.infinite_markov_enumerable_implementation import InfiniteMarkovEnumerable as IME

def MyFunction():
    """this is a function"""
    return 2

__all__ = [
    'FMES',
    'IMES',
    'IME',
    'MyFunction'
]

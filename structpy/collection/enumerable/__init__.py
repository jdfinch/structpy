
"""
Defines a potentially infinite sequence of values that can be iterated
over, where each value is derived from an update of the previous one.

Test.
"""

from structpy.language.specification.factory import Factory

from structpy.collection.enumerable.finite_markov_enumerable import FiniteMarkovEnumerableSpec
from structpy.collection.enumerable.infinite_markov_enumerable import InfiniteMarkovEnumerableSpec

@Factory
def Enumerable(type='markov', finite=True, implementation='standard'):
    return FiniteMarkovEnumerableSpec, InfiniteMarkovEnumerableSpec

if __name__ == '__main__':
    enumerable = Enumerable(finite=False)
    print(enumerable)


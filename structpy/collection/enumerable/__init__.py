
from structpy.collection.enumerable.finite_markov_enumerable import FiniteMarkovEnumerableSpecification
from structpy.collection.enumerable.infinite_markov_enumerable import InfiniteMarkovEnumerable


def Enumerable(type='markov', finite=True):
    if type == 'markov':
        if finite:
            return FiniteMarkovEnumerableSpecification.__implementation__()
        else:
            return InfiniteMarkovEnumerable.__implementation__()


if __name__ == '__main__':

    class MyEnumerable(Enumerable()):

        def update(self, value):
            return value + 1

        def end(self, value):
            return value == 10

    for x in Enumerable(initial=1, update=(lambda value: value + 1), end=(lambda value: value == 10)):
        print(x)


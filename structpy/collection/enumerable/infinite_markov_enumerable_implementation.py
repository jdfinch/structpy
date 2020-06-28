
from structpy import implementation
from structpy.collection.enumerable.infinite_markov_enumerable import InfiniteMarkovEnumerableSpec

from abc import ABC, abstractmethod

@implementation(InfiniteMarkovEnumerableSpec)
class InfiniteMarkovEnumerable(ABC):

    __kwargs__ = {
        'implementation': 'standard'
    }

    def __init__(self, initial):
        self.initial = initial
        self.value = self.initial

    @abstractmethod
    def update(self, value):
        pass

    def next(self):
        return self.__next__()

    def reset(self):
        self.value = self.initial
        return self

    def __iter__(self):
        return self

    def __next__(self):
        value = self.value
        self.value = self.update(self.value)
        return value


if __name__ == '__main__':
    print(InfiniteMarkovEnumerableSpec.__verify__(InfiniteMarkovEnumerable))
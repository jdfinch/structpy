
from structpy import specification, implementation


@specification
class InfiniteMarkovEnumerableSpec:
    """
    Define a sequence iterator that generates each
    value based on the previous value.
    """

    __kwargs__ = {
        'type': 'markov',
        'finite': False
    }

    @specification.init
    def init(Struct):
        """
        Example of MarkovEnumerable for positive odd integers
        """
        class EveryOtherInt(Struct):
            def update(self, x):
                return x + 2
        return EveryOtherInt(1)

    def __iter__(struct):
        """
        MarkovEnumerable can be used by looping over it.
        """
        for value in struct:
            assert value % 2 == 1
            if value == 7:
                return

    def next(struct):
        """
        Use .next() or built-in next function to get the next
        value from the MarkovEnumerable
        """
        assert struct.next() == 9
        assert next(struct) == 11

    def reset(struct):
        """
        Reset the value to the MarkovEnumerable's initial value.
        """
        struct.reset()
        for value in struct:
            assert value == 1
            break
        for value in struct:
            assert value == 3
            break
        struct.reset()
        for value in struct:
            assert value == 1
            break
        assert struct.reset() == struct


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
    print(InfiniteMarkovEnumerableSpec.__verify__())
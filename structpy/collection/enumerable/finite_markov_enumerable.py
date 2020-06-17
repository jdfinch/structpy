
from structpy.language import specification, implementation


@specification
class FiniteMarkovEnumerableSpec:
    """
    Define a sequence iterator that generates each
    value based on the previous value.

    A boolean end function is specified to define
    the end of the sequence.
    """

    __kwargs__ = {
        'type': 'markov',
        'finite': True
    }

    @specification.init
    def FINITE_MARKOV_ENUMERABLE(Struct):
        """
        Example of MarkovEnumerable for positive odd single-digit integers
        """
        class EveryOtherIntToTen(Struct):
            def update(self, x):
                return x + 2
            def end(self, x):
                return x >= 10
        return EveryOtherIntToTen(1)


    def iter(enumerable):
        """
        MarkovEnumerable can be used by looping over it.
        """
        for value in enumerable:
            assert value % 2 == 1


    def reset(enumerable):
        """
        Reset the value to the MarkovEnumerable's initial value.
        """
        enumerable.reset()
        for value in enumerable:
            assert value == 1
            break
        for value in enumerable:
            assert value == 3
            break
        enumerable.reset()
        for value in enumerable:
            assert value == 1
            break
        assert enumerable.reset() == enumerable


    def next(enumerable):
        """
        Use .next() or built-in next function to get the next
        value from the MarkovEnumerable
        """
        assert enumerable.next() == 1
        assert next(enumerable) == 3


from abc import ABC, abstractmethod

@implementation(FiniteMarkovEnumerableSpec)
class FiniteMarkovEnumerable(ABC):

    __kwargs__ = {
        'implementation': 'standard'
    }

    def __init__(self, initial):
        self.initial = initial
        self.value = self.initial

    @abstractmethod
    def update(self, value):
        pass

    @abstractmethod
    def end(self, value):
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
        if self.end(value):
            raise StopIteration
        return value


if __name__ == '__main__':
    print(FiniteMarkovEnumerableSpec.__verify__())
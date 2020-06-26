
from structpy.language import specification, implementation

@specification
class FiniteSet:
    """
    Unordered collection of elements

    Differs from python set by being hashable
    """

    @specification.init
    def init(Struct, elements=None):
        """
        `elements` is an iterable of elements that are added to the set
        on construction
        """
        elements = {1, 2, 3, 5}
        return Struct(elements)

    @specification.init
    def SET_OPERATIONS(Struct):
        return Struct


    def union(struct, other):
        assert struct((1, 2, 3, 5)) | struct((5, 6, 7)) == struct((1, 2, 3, 5, 6, 7))


    def intersection(struct, other):
        assert struct((1, 2, 3, 5)) & struct((2, 3, 4)) == struct((2, 3))


    def difference(struct, other):
        assert struct((1, 2, 3, 5)) - struct((5, 6)) == struct((1, 2, 3))


    def symmetric_difference(struct, other):
        assert struct((1, 2, 3, 5)) ^ struct((3, 4, 5)) == struct((1, 2, 4))

    @specification.init
    def __hash__(struct):
        """
        FiniteSet is hashable, using the same hash function as built-in frozenset
        """
        set = struct((1, 2, 3, 5))
        equivalent_set = frozenset((1, 2, 3, 5))
        assert equivalent_set == set
        outer_set = {set}
        assert equivalent_set in outer_set


@implementation(FiniteSet)
class Set(set):
    """
    Simple implementation of FiniteSet by overriding python set `__hash__` and `__eq__`
    """

    def __eq__(self, other):
        return set.__eq__(self, other)

    def __hash__(self):
        return hash(frozenset(self))

if __name__ == '__main__':
    print(FiniteSet.__verify__())
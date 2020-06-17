
from structpy.language import specification, implementation

@specification
class FiniteSet:
    """
    Unordered collection of elements

    Differs from python set by being hashable
    """

    @specification.init
    def init(Struct, elements=None):
        elements = {1, 2, 3, 5}
        return Struct(elements)


    def union(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) | Struct((5, 6, 7)) == Struct((1, 2, 3, 5, 6, 7))


    def intersection(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) & Struct((2, 3, 4)) == Struct((2, 3))


    def difference(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) - Struct((5, 6)) == Struct((1, 2, 3))


    def symmetric_difference(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) ^ Struct((3, 4, 5)) == Struct((1, 2, 4))


    def __hash__(set):
        """
        FiniteSet is hashable, using the same hash function as built-in frozenset
        """
        equivalent_set = frozenset((1, 2, 3, 5))
        assert equivalent_set == set
        outer_set = {set}
        assert equivalent_set in outer_set


@implementation(FiniteSet)
class Set1(set):

    def __eq__(self, other):
        return set.__eq__(self, other)

    def __hash__(self):
        return hash(frozenset(self))

if __name__ == '__main__':
    FiniteSet.verify()
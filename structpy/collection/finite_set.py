
from structpy.language import Specification, Implementation

@Specification
class FiniteSet:
    """
    Unordered collection of elements

    Differs from python set by being hashable
    """

    @Specification.construction
    def init(Struct, elements=None):
        elements = {1, 2, 3, 5}
        return Struct(elements)

    @Specification.definition
    def union(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) | Struct((5, 6, 7)) == Struct((1, 2, 3, 5, 6, 7))

    @Specification.definition
    def intersection(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) & Struct((2, 3, 4)) == Struct((2, 3))

    @Specification.definition
    def difference(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) - Struct((5, 6)) == Struct((1, 2, 3))

    @Specification.definition
    def symmetric_difference(set, other):
        Struct = set.__class__
        assert Struct((1, 2, 3, 5)) ^ Struct((3, 4, 5)) == Struct((1, 2, 4))

    @Specification.definition
    def __hash__(set):
        """
        FiniteSet is hashable, using the same hash function as built-in frozenset
        """
        equivalent_set = frozenset((1, 2, 3, 5))
        assert equivalent_set == set
        outer_set = {set}
        assert equivalent_set in outer_set


@Implementation(FiniteSet)
class Set1(set):

    def __eq__(self, other):
        return set.__eq__(self, other)

    def __hash__(self):
        return hash(frozenset(self))

if __name__ == '__main__':
    FiniteSet.verify()
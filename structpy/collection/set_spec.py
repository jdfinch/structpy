
from structpy.language import specification

@specification
class SetSpec:
    """
    Unordered, finite collection of elements

    Differs from python Set by being hashable
    """

    @specification.init
    def init(Set, elements=None):
        """
        `elements` is an iterable of elements that are added to the Set
        on consetion
        """
        elements = {1, 2, 3, 5}
        return Set(elements)

    @specification.init
    def SET_OPERATIONS(Set):
        """
        Set can be conseted using standard Set operations,
        e.g. `& | - ^`
        """
        return Set

    def union(Set, other):
        """
        `s1 | s2`
        """
        assert Set((1, 2, 3, 5)) | Set((5, 6, 7)) == Set((1, 2, 3, 5, 6, 7))


    def intersection(Set, other):
        """
        `s1 & s2`
        """
        assert Set((1, 2, 3, 5)) & Set((2, 3, 4)) == Set((2, 3))


    def difference(Set, other):
        """
        `s1 - s2`
        """
        assert Set((1, 2, 3, 5)) - Set((5, 6)) == Set((1, 2, 3))


    def symmetric_difference(Set, other):
        """
        `s1 ^ s2`
        """
        assert Set((1, 2, 3, 5)) ^ Set((3, 4, 5)) == Set((1, 2, 4))

    @specification.init
    def __hash__(Set):
        """
        FiniteSet is hashable, using the same hash function as built-in frozenset
        """
        set = Set((1, 2, 3, 5))
        equivalent_set = frozenset((1, 2, 3, 5))
        assert equivalent_set == set
        outer_set = {set}
        assert equivalent_set in outer_set



from structpy.language import Specification


class Set(Specification):
    """
    Unordered collection of elements

    Differs from python set by being hashable
    """

    @Specification.example
    def set_of_integers(self, Struct):
        s = Struct(1, 2, 4, 5)
        s.add(6)
        assert s == {1, 2, 4, 5, 6}
        assert 2 in s
        assert 3 not in s

        s_intersected = s & {2, 4, 6, 8}
        assert s_intersected == {2, 4, 6}
        s_unioned = s | {3, 7}
        assert s_unioned == {1, 2, 3, 4, 5, 6, 7}
        s_diffed = s - {4, 5, 6}
        assert s_diffed == {1, 2}

        my_dict = {Struct(1, 2, 3): 6, Struct(4, 5): 9}
        assert my_dict[Struct(1, 2, 3)] == 6
        assert my_dict[Struct(4, 5)] == 9

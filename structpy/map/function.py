
from structpy.language import Specification


class Function(Specification):
    """
    Maps a set of keys to values, much like a python dictionary.

    Keys to values is a many to one relation
    """

    @Specification.example
    def mapping_with_function(self, Struct):
        function = Struct({'one': 1, 'two': 2})
        function['uno'] = 1
        assert function['one'] == 1
        assert function['two'] == 2
        assert function['uno'] == 1
        assert function.map_sequence(['one', 'two', 'uno']) == [1, 2, 1]

    @Specification.example
    def reverse_mapping_of_function(self, Struct):
        function = Struct({'one': 1, 'two': 2, 'uno': 1, 'tres': 3})
        assert function.reverse[1] == {'one', 'uno'}
        assert function.reverse[2] == {'two'}
        assert function.reverse[3] == {'tres'}








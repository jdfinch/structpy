
from structpy.language import Specification


class Lookup(Specification):
    """
    Maps a key to a set of values, much like a python dictionary of sets.
    This mapping is the reverse of a Function mapping.
    Each value has a unique key.

    Keys to values is one to many
    """

    @Specification.example
    def mapping_with_lookup(self, Struct):
        lookup = Struct({1: {'one', 'uno'}, 2: {'two'}})
        assert lookup[1] == {'one', 'uno'}
        lookup[3].add('tres')
        lookup[3].add('three', 'set')
        assert lookup[1] == {'one', 'uno'}
        assert 'three' in lookup[3]

        # cant have a value associated with more than one key
        lookup[3].add('one')
        assert 'one' in lookup[3]
        assert 'one' not in lookup[1]

    @Specification.example
    def reverse_mapping_of_sequence(self, Struct):
        lookup = Struct({1: {'one', 'uno'}, 2: {'two'}, 3: {'three', 'tres', 'set'}})
        assert lookup.reverse['one'] == 1
        assert lookup.reverse['uno'] == 1
        assert lookup.reverse['two'] == 2
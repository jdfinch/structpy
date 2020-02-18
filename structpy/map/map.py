
from structpy.language import Specification


class Map(Specification):
    """
    Arbitrary many-to-many mapping of a finite domain and codomain.

    Reverses to another mapping.
    """

    @Specification.example
    def mapping_example(self, Struct):
        mapping = Struct({'dog': {'barks', 'mammal'}, 'bat': {'flies', 'mammal'}})
        mapping['bird'].add('flies')
        mapping['bird'].add('feathers')
        assert 'feathers' in mapping['bird']
        assert 'barks' in mapping['dog']
        assert 'mammal' in mapping['dog']

    def reverse_of_mapping(self, Struct):
        mapping = Struct({'dog': {'barks', 'mammal'}, 'bat': {'flies', 'mammal'}})
        assert mapping.reverse['mammal'] == {'dog', 'bat'}
        assert mapping.reverse['barks'] == {'dog'}
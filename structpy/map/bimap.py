
from structpy.language import Specification


class Bimap(Specification):
    """
    Bijective Mapping

    one-to-one mapping between keys and values
    """

    @Specification.example
    def mapping_with_bimap(self, Struct):
        bimap = Struct({'one': 1, 'two': 2, 'three': 3})
        bimap['four'] = 4
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['four'] == 4
        bimap['one'] = 2
        assert bimap['one'] == 2
        assert 'two' not in bimap

    @Specification.example
    def reverse_mapping_of_bimap(self, Struct):
        bimap = Struct({'one': 1, 'two': 2, 'three': 3})
        assert bimap.reverse[1] == 'one'
        assert bimap.reverse[3] == 'three'

from structpy.language import Specification


class Bimap(Specification):
    """
    Bijective Mapping

    one-to-one mapping between keys and values
    """

    @Specification.construction
    def number_bimap(self, Struct):
        return Struct({'one': 1, 'two': 2, 'three': 3})

    @Specification.definition
    def __getitem__(bimap, item):
        """

        """
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['three'] == 3

    @Specification.definition
    def __setitem__(bimap, key, value):
        """

        """
        bimap['four'] = 4
        bimap['five'] = 5
        assert bimap['four'] == 4
        assert bimap['five'] == 5

        # overwrite key-value pair
        bimap['one'] = 0
        assert bimap['one'] == 0


if __name__ == '__main__':
    Bimap.verify_implementations()






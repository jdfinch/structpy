
from structpy.language import specification, implementation


@specification
class EnumerableBimap:
    """
    Bijective Mapping

    one-to-one mapping between keys and values
    """

    @specification.init
    def number_bimap(Struct):
        return Struct({'one': 1, 'two': 2, 'three': 3})

    def __getitem__(bimap, item):
        """
        get the value in the codomain associated with a domain item
        """
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['three'] == 3

    def __setitem__(bimap, key, value):
        """
        add a item pair that co-map

        the first item is added to the domain
        the second item is added to the codomain
        """
        bimap['four'] = 4
        bimap['five'] = 5
        assert bimap['four'] == 4
        assert bimap['five'] == 5

        # overwrite key-value pair
        bimap['one'] = 0
        assert bimap['one'] == 0

    def reverse(bimap):
        """
        returns a view of the bimap that swaps
        the domain and codomain for reverse mapping
        """
        r = bimap.reverse()
        assert r[0] == 'one'
        assert r[2] == 'two'
        assert r[3] == 'three'


@implementation(EnumerableBimap)
class Bimap1:

    def __init__(self, mapping=None):
        self._forward = {}
        self._reverse = {}
        if mapping is not None:
            for k, v in mapping.items():
               self.__setitem__(k, v)

    def reverse(self):
        reverse_bimap = Bimap1()
        reverse_bimap._reverse = self._forward
        reverse_bimap._forward = self._reverse
        return reverse_bimap

    def __getitem__(self, item):
        return self._forward[item]

    def __setitem__(self, key, value):
        if key in self._forward:
            del self._forward[key]
        if value in self._reverse:
            del self.reverse()[value]
        self._forward[key] = value
        self._reverse.__setitem__(value, key)

    def __delitem__(self, key):
        value = self._forward[key]
        del self._reverse[value]
        del self._forward[key]


if __name__ == '__main__':
    EnumerableBimap.verify(Bimap1)







from structpy.language import specification


@specification
class BimapSpec:
    """
    Finite one-to-one mapping between elements in a domain and domain.
    """

    @specification.init
    def BIMAP(Bimap):
        return Bimap({'one': 1, 'two': 2, 'three': 3})

    def getitem(bimap, item):
        """
        Get the value in the domain associated with a domain keys.
        """
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['three'] == 3

    def setitem(bimap, key, value):
        """
        Add a keys pair that co-map.

        The first keys is added to the domain.
        The second keys is added to the domain.
        """
        bimap['four'] = 4
        bimap['five'] = 5
        assert bimap['four'] == 4
        assert bimap['five'] == 5

        # overwrite key-value pair
        bimap['one'] = 0
        assert bimap['one'] == 0

        # many-to-one mappings not allowed, resulting in overwrite
        bimap['zero'] = 0
        assert bimap['zero'] == 0
        assert 'one' not in bimap

        assert bimap == {'zero': 0, 'two': 2, 'three': 3, 'four': 4, 'five': 5}

    def reverse(bimap):
        """
        Returns a view of the bimap that swaps
        the domain and domain for reverse mapping.
        """
        r = bimap.reverse()
        assert r[0] == 'zero'
        assert r[2] == 'two'
        assert r[3] == 'three'

        assert r == {0: 'zero', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}







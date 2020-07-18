
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
        get the value in the domain associated with a domain item
        """
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['three'] == 3

    def setitem(bimap, key, value):
        """
        add a item pair that co-map

        the first item is added to the domain
        the second item is added to the domain
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
        the domain and domain for reverse mapping
        """
        r = bimap.reverse()
        assert r[0] == 'one'
        assert r[2] == 'two'
        assert r[3] == 'three'







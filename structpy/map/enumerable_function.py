
from structpy.language import spec, Implementation


@spec
class EnumerableFunction:
    """
    Function Mapping

    many-to-one mapping between keys and values
    """

    @spec.init
    def number_bimap(Struct):
        return Struct({'one': 1, 'two': 2, 'uno': 1})

    @spec.prop
    def __getitem__(bimap, item):
        """
        get the value in the codomain associated with a domain item
        """
        assert bimap['one'] == 1
        assert bimap['two'] == 2
        assert bimap['three'] == 3

    @spec.prop
    def __setitem__(bimap, key, value):
        """
        add a item pair that co-map

        the first item is added to the domain
        the second item is added to the codomain
        """
        bimap['dos'] = 2
        assert bimap['dos'] == 2

        # overwrite key-value pair
        bimap['dos'] = 3
        assert bimap['dos'] == 3

    @spec.prop
    def reverse(bimap):
        """
        returns a lookup (one-to-many mapping) representing
        a mapping with domain and codomain swapped
        """
        r = bimap.reverse()
        assert 'one' in r[1]
        assert 'uno' in r[1]
        assert 'two' in r[2]







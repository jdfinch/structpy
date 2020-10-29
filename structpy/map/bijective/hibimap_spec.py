
from structpy.language import specification


@specification
class HibimapSpec:
    """
    Hierarchical bijective mapping between finite domain and codomain.
    """

    @specification.init
    def HIBIMAP(Hibimap, order, mapping=None):
        return Hibimap(2, {
            1: {
                'english': {'abbr': 'o', 'full': 'one'},
                'spanish': {'abbr': 'u', 'full': 'uno'}
            },
            2: {
                'english': {'abbr': 't'}
            }
        })

    def getitem(hibimap, item):
        """
        Get the value in the domain associated with a domain keys.
        """
        assert hibimap[1, 'english', 'full'] == 'one'
        assert hibimap[2, 'english', 'abbr'] == 't'

    def setitem(hibimap, key, value):
        """
        Add a keys pair that co-map.

        The first keys is added to the domain.
        The second keys is added to the domain.
        """
        hibimap[2, 'english', 'full'] = '222'
        assert hibimap[2, 'english', 'full'] == '222'

        # overwrite key-value pair
        hibimap[2, 'english', 'full'] = 'three'
        assert hibimap[2, 'english', 'full'] == 'three'

        # many-to-one mappings not allowed, resulting in overwrite
        hibimap[3, 'english', 'full'] = 'three'
        assert hibimap[3, 'english', 'full'] == 'three'
        assert (2, 'english', 'full') not in hibimap

    def reverse(hibimap):
        """
        Returns a view of the bimap that swaps
        the domain and codomain for reverse mapping.
        """
        r = hibimap.reverse()
        assert r['three'] == (3, 'english', 'full')
        assert r['o'] == (1, 'english', 'abbr')






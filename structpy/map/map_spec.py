
from structpy import specification


@specification
class MapSpec:
    """
    Finite many-to-many mapping between a domain and domain.
    """

    @specification.init
    def MAP(Map, mapping=None):
        map = Map({
                'avengers': {'scarlett', 'chris'},
                'marriage story': {'scarlett', 'adam'},
                'star wars': {'adam'}
            })
        return map

    def getitem(map, item):
        """
        Get a reference to the elements in the domain associated
        with domain element item.
        """
        assert map['avengers'] == {'scarlett', 'chris'}
        assert map['star wars'] == {'adam'}

        # Elements can be added individually using the reference
        map['avengers'].add('robert')
        assert map['avengers'] == {'scarlett', 'chris', 'robert'}

    def additem(map, key, values):
        """
        Set the domain elements associated with a key to all the
        elements present in values.

        Each element of values is added to the domain, without
        a direct reference to the provided values object.
        """
        map['star wars'].add('adam')
        map['star wars'].update(['daisy'])
        assert map['star wars'] == {'adam', 'daisy'}

    def delitem(map, element):
        """
        Remove an element from the map domain.
        """
        map['captain america']
        assert map['captain america'] == set()
        assert 'captain america' in map
        del map['captain america']
        assert 'captain america' not in map

    def update(map, mapping):
        """
        Join a many-to-many mapping of elements to the map.

        `mapping` should be like `dict<key: iterable<value>>`.
        """
        map.update(
            {'harry potter': {'rupert', 'emma'},
             'twilight': {'kristen'}
            }
        )

    def reverse(map):
        """
        Returns a view of the map that swaps the domain and domain
        for reverse mapping.
        """
        r = map.reverse()
        assert r['chris'] == {'avengers'}
        assert r['adam'] == {'marriage story', 'star wars'}
